import os
import json
from pathlib import Path


def manual_validation():
    """
    עובר על כל קבצי הבדיקה מ-Stack Overflow ומאפשר סימון ידני
    """
    # תיקיית הקבצים - בדוק איפה אנחנו
    if os.path.exists("test_samples"):
        test_dir = "test_samples"  # אם אנחנו בתוך tests
    else:
        test_dir = "tests/test_samples"  # אם אנחנו בתיקיה הראשית

    # חיפוש כל קבצי Stack Overflow
    so_files = []
    for file in os.listdir(test_dir):
        if "stackoverflow" in file and file.endswith(".txt"):
            so_files.append(file)

    print(f"נמצאו {len(so_files)} קבצי Stack Overflow לבדיקה\n")

    # מילון לשמירת התוצאות
    validation_results = {}

    # אם יש קובץ תוצאות קיים, טען אותו
    results_file = "manual_validation_results.json"
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            validation_results = json.load(f)
        print(f"נטענו {len(validation_results)} תוצאות קיימות\n")

    # עבור על כל קובץ
    for i, filename in enumerate(so_files):
        # אם כבר בדקנו את הקובץ, דלג
        if filename in validation_results:
            continue

        filepath = os.path.join(test_dir, filename)

        print(f"\n{'=' * 60}")
        print(f"קובץ {i + 1}/{len(so_files)}: {filename}")
        print(f"{'=' * 60}\n")

        # קרא את תוכן הקובץ
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # הצג את התוכן
        lines = content.split('\n')
        print("תוכן הקובץ (עד 50 שורות):")
        print("-" * 40)
        for j, line in enumerate(lines[:50]):
            print(f"{j + 1:3}: {line}")
        if len(lines) > 50:
            print(f"\n... ועוד {len(lines) - 50} שורות")

        # קבל החלטה מהמשתמש
        print("\n" + "-" * 40)
        print("האם הקובץ מכיל קוד משמעותי?")
        print("1 = כן, מכיל קוד")
        print("2 = לא, רק טקסט")
        print("3 = מכיל קוד אבל מעורבב עם הרבה טקסט")
        print("s = דלג (skip)")
        print("q = צא (quit)")

        while True:
            choice = input("\nהבחירה שלך: ").strip().lower()

            if choice == 'q':
                # שמור ויצא
                with open(results_file, 'w') as f:
                    json.dump(validation_results, f, indent=2)
                print(f"\nנשמרו {len(validation_results)} תוצאות")
                return

            elif choice == 's':
                print("דילוג...")
                break

            elif choice in ['1', '2', '3']:
                validation_results[filename] = {
                    'contains_code': choice in ['1', '3'],
                    'code_type': {
                        '1': 'pure_code',
                        '2': 'no_code',
                        '3': 'mixed'
                    }[choice],
                    'expected_detection': choice in ['1', '3']
                }

                # שמור אחרי כל קובץ
                with open(results_file, 'w') as f:
                    json.dump(validation_results, f, indent=2)

                print(f"✓ נשמר: {validation_results[filename]}")
                break
            else:
                print("בחירה לא חוקית, נסה שוב")

    print(f"\n\nסיימנו! בדקנו {len(validation_results)} קבצים")

    # הצג סיכום
    code_files = sum(1 for v in validation_results.values() if v['contains_code'])
    no_code = sum(1 for v in validation_results.values() if v['code_type'] == 'no_code')
    mixed = sum(1 for v in validation_results.values() if v['code_type'] == 'mixed')

    print(f"\nסיכום:")
    print(f"- קבצי קוד טהור: {code_files - mixed}")
    print(f"- קבצים מעורבבים: {mixed}")
    print(f"- קבצים ללא קוד: {no_code}")


def compare_with_detection_results():
    """
    משווה את התוצאות הידניות עם תוצאות ה-CodeDetector
    """
    import subprocess

    # בדוק אם יש תוצאות ידניות
    if not os.path.exists('manual_validation_results.json'):
        print("❌ לא נמצא קובץ manual_validation_results.json")
        print("הרץ קודם: python manual_validation.py")
        return

    # טען תוצאות ידניות
    with open('manual_validation_results.json', 'r') as f:
        manual_results = json.load(f)

    print(f"נטענו {len(manual_results)} תוצאות ידניות\n")

    # הרץ את CodeDetector על הקבצים
    print("מריץ CodeDetector על הקבצים...")

    # תיקון ה-import - הוסף את התיקיה הראשית ל-path
    import sys
    sys.path.append('..')  # הוסף את התיקיה הראשית

    from extractor.code_detector import CodeDetector

    detector = CodeDetector()
    detection_results = {}

    # תיקון הנתיב - הקבצים בתיקיית test_samples
    test_dir = "test_samples"  # התת-תיקייה הנכונה

    # בדוק כל קובץ שסימנו ידנית
    for filename, manual_label in manual_results.items():
        filepath = os.path.join(test_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️  לא נמצא: {filepath}")
            continue

        # קרא את הקובץ
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # הרץ את הdetector
        detected_blocks = detector.detect_code(content)

        # שמור תוצאה
        detection_results[filename] = {
            'detected': len(detected_blocks) > 0,
            'num_blocks': len(detected_blocks),
            'manual_says_code': manual_label['contains_code'],
            'code_type': manual_label['code_type']
        }

    # חשב סטטיסטיקות
    correct_detections = 0
    false_positives = 0
    false_negatives = 0

    for filename, result in detection_results.items():
        detected = result['detected']
        should_detect = result['manual_says_code']

        if detected and should_detect:
            correct_detections += 1
        elif detected and not should_detect:
            false_positives += 1
        elif not detected and should_detect:
            false_negatives += 1
        else:  # not detected and not should_detect
            correct_detections += 1

    total = len(detection_results)
    accuracy = (correct_detections / total * 100) if total > 0 else 0

    print(f"\n{'=' * 50}")
    print(f"תוצאות ההשוואה:")
    print(f"{'=' * 50}")
    print(f"סה\"כ קבצים שנבדקו: {total}")
    print(f"✅ זיהויים נכונים: {correct_detections}")
    print(f"❌ False Positives: {false_positives} (זיהה קוד כשאין)")
    print(f"❌ False Negatives: {false_negatives} (לא זיהה קוד כשיש)")
    print(f"📊 דיוק כולל: {accuracy:.1f}%")

    # הצג פירוט של טעויות
    if false_positives > 0:
        print(f"\n🔴 False Positives:")
        for filename, result in detection_results.items():
            if result['detected'] and not result['manual_says_code']:
                print(f"  - {filename}")

    if false_negatives > 0:
        print(f"\n🔴 False Negatives:")
        for filename, result in detection_results.items():
            if not result['detected'] and result['manual_says_code']:
                print(f"  - {filename} (type: {result['code_type']})")

    # שמור תוצאות מפורטות
    with open('comparison_results.json', 'w') as f:
        json.dump(detection_results, f, indent=2)
    print(f"\n💾 תוצאות מפורטות נשמרו ב-comparison_results.json")


if __name__ == "__main__":
    print("Manual Validation Tool for Stack Overflow Files")
    print("=" * 50)

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--compare':
        compare_with_detection_results()
    else:
        manual_validation()