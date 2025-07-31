import json
from datetime import datetime

def generate_detailed_report():
    """יוצר דוח מפורט של תוצאות ההשוואה"""
    
    # טען את התוצאות
    try:
        with open('comparison_results.json', 'r') as f:
            results = json.load(f)
        
        with open('manual_validation_results.json', 'r') as f:
            manual = json.load(f)
    except FileNotFoundError:
        print("❌ לא נמצאו קבצי התוצאות")
        return
    
    # חשב סטטיסטיקות
    total = len(results)
    correct = 0
    false_positives = []
    false_negatives = []
    
    for filename, result in results.items():
        detected = result['detected']
        should_detect = result['manual_says_code']
        
        if detected == should_detect:
            correct += 1
        elif detected and not should_detect:
            false_positives.append(filename)
        else:
            false_negatives.append((filename, result['code_type']))
    
    # צור את הדוח
    report = []
    report.append("=" * 80)
    report.append("VALIDATION REPORT - MANUAL VS AUTOMATIC DETECTION")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # סיכום כללי
    report.append("SUMMARY")
    report.append("-" * 40)
    report.append(f"Total files tested: {total}")
    report.append(f"Correct Detections: {correct} ({correct/total*100:.1f}%)")
    report.append(f"False positives: {len(false_positives)} ({len(false_positives)/total*100:.1f}%)")
    report.append(f"Miss Detect: {len(false_negatives)} ({len(false_negatives)/total*100:.1f}%)")
    report.append("")
    
    # פירוט לפי שפה
    report.append("BREAKDOWN BY LANGUAGE")
    report.append("-" * 40)
    
    python_files = [f for f in results if f.startswith('python_')]
    c_files = [f for f in results if f.startswith('c_')]
    
    # Python
    python_correct = sum(1 for f in python_files if results[f]['detected'] == results[f]['manual_says_code'])
    report.append(f"Python files: {len(python_files)}")
    report.append(f"  Correct: {python_correct} ({python_correct/len(python_files)*100:.1f}%)")
    report.append(f"  Errors: {len(python_files) - python_correct}")
    
    # C
    c_correct = sum(1 for f in c_files if results[f]['detected'] == results[f]['manual_says_code'])
    report.append(f"\nC files: {len(c_files)}")
    report.append(f"  Correct: {c_correct} ({c_correct/len(c_files)*100:.1f}%)")
    report.append(f"  Errors: {len(c_files) - c_correct}")
    report.append("")
    
    # False Positives
    report.append("FALSE POSITIVES (Detected code when there isn't)")
    report.append("-" * 40)
    for i, fp in enumerate(false_positives, 1):
        manual_info = manual.get(fp, {})
        report.append(f"{i}. {fp}")
        report.append(f"   Manual classification: {manual_info.get('code_type', 'Unknown')}")
        report.append(f"   Number of blocks detected: {results[fp]['num_blocks']}")
    report.append("")
    
    # False Negatives
    report.append("FALSE NEGATIVES (Didn't detect code when there is)")
    report.append("-" * 40)
    for i, (fn, code_type) in enumerate(false_negatives, 1):
        report.append(f"{i}. {fn}")
        report.append(f"   Manual classification: {code_type}")
        report.append(f"   Expected to detect: Yes")
    report.append("")
    
    # פירוט מלא
    report.append("DETAILED RESULTS FOR ALL FILES")
    report.append("-" * 40)
    report.append(f"{'Filename':<60} {'Manual':<10} {'Detected':<10} {'Result':<10}")
    report.append("-" * 90)
    
    for filename in sorted(results.keys()):
        result = results[filename]
        manual_says = "Code" if result['manual_says_code'] else "No Code"
        detected = "Code" if result['detected'] else "No Code"
        status = "✓ OK" if result['detected'] == result['manual_says_code'] else "✗ ERROR"
        
        report.append(f"{filename:<60} {manual_says:<10} {detected:<10} {status:<10}")
    
    # שמור לקובץ
    output_file = "validation_report_detailed.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✅ הדוח נשמר ב: {output_file}")
    print(f"📄 גודל הדוח: {len(report)} שורות")
    
    # הצג תקציר
    print("\nתקציר:")
    print(f"- Correct Detection: {correct/total*100:.1f}%")
    print(f"- False Positives: {len(false_positives)}")
    print(f"- Miss Detect : {len(false_negatives)}")

if __name__ == "__main__":
    generate_detailed_report()
