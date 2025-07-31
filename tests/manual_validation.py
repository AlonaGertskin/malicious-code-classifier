import os
import json
from pathlib import Path


def manual_validation():
    """
    Iterate through all Stack Overflow test files and allow manual labeling
    """
    # Test files directory - check where we are
    if os.path.exists("test_samples"):
        test_dir = "test_samples"  # If we're inside tests
    else:
        test_dir = "tests/test_samples"  # If we're in the root directory

    # Search for all Stack Overflow files
    so_files = []
    for file in os.listdir(test_dir):
        if "stackoverflow" in file and file.endswith(".txt"):
            so_files.append(file)

    print(f"Found {len(so_files)} Stack Overflow files for validation\n")

    # Dictionary to save results
    validation_results = {}

    # If results file exists, load it
    results_file = "manual_validation_results.json"
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            validation_results = json.load(f)
        print(f"Loaded {len(validation_results)} existing results\n")

    # Iterate through each file
    for i, filename in enumerate(so_files):
        # If we already validated this file, skip
        if filename in validation_results:
            continue

        filepath = os.path.join(test_dir, filename)

        print(f"\n{'=' * 60}")
        print(f"File {i + 1}/{len(so_files)}: {filename}")
        print(f"{'=' * 60}\n")

        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Display content
        lines = content.split('\n')
        print("File content (up to 50 lines):")
        print("-" * 40)
        for j, line in enumerate(lines[:50]):
            print(f"{j + 1:3}: {line}")
        if len(lines) > 50:
            print(f"\n... and {len(lines) - 50} more lines")

        # Get user decision
        print("\n" + "-" * 40)
        print("Does this file contain meaningful code?")
        print("1 = Yes, contains code")
        print("2 = No, only text")
        print("3 = Contains code but mixed with lots of text")
        print("s = Skip")
        print("q = Quit")

        while True:
            choice = input("\nYour choice: ").strip().lower()

            if choice == 'q':
                # Save and exit
                with open(results_file, 'w') as f:
                    json.dump(validation_results, f, indent=2)
                print(f"\nSaved {len(validation_results)} results")
                return

            elif choice == 's':
                print("Skipping...")
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

                # Save after each file
                with open(results_file, 'w') as f:
                    json.dump(validation_results, f, indent=2)

                print(f"✓ Saved: {validation_results[filename]}")
                break
            else:
                print("Invalid choice, please try again")

    print(f"\n\nFinished! Validated {len(validation_results)} files")

    # Display summary
    code_files = sum(1 for v in validation_results.values() if v['contains_code'])
    no_code = sum(1 for v in validation_results.values() if v['code_type'] == 'no_code')
    mixed = sum(1 for v in validation_results.values() if v['code_type'] == 'mixed')

    print(f"\nSummary:")
    print(f"- Pure code files: {code_files - mixed}")
    print(f"- Mixed files: {mixed}")
    print(f"- Files without code: {no_code}")


def compare_with_detection_results():
    """
    Compare manual validation results with CodeDetector results
    """
    import subprocess

    # Check if manual results exist
    if not os.path.exists('manual_validation_results.json'):
        print("❌ File manual_validation_results.json not found")
        print("Run first: python manual_validation.py")
        return

    # Load manual results
    with open('manual_validation_results.json', 'r') as f:
        manual_results = json.load(f)

    print(f"Loaded {len(manual_results)} manual results\n")

    # Run CodeDetector on files
    print("Running CodeDetector on files...")

    # Fix import - add root directory to path
    import sys
    sys.path.append('..')  # Add root directory

    from extractor.code_detector import CodeDetector

    detector = CodeDetector()
    detection_results = {}

    # Fix path - files are in test_samples directory
    test_dir = "test_samples"  # The correct subdirectory

    # Check each manually labeled file
    for filename, manual_label in manual_results.items():
        filepath = os.path.join(test_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️  Not found: {filepath}")
            continue

        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Run the detector
        detected_blocks = detector.detect_code(content)

        # Save result
        detection_results[filename] = {
            'detected': len(detected_blocks) > 0,
            'num_blocks': len(detected_blocks),
            'manual_says_code': manual_label['contains_code'],
            'code_type': manual_label['code_type']
        }

    # Calculate statistics
    correct_detections = 0
    false_positives = 0
    miss_detects = 0

    for filename, result in detection_results.items():
        detected = result['detected']
        should_detect = result['manual_says_code']

        if detected and should_detect:
            correct_detections += 1
        elif detected and not should_detect:
            false_positives += 1
        elif not detected and should_detect:
            miss_detects += 1
        else:  # not detected and not should_detect
            correct_detections += 1

    total = len(detection_results)
    accuracy = (correct_detections / total * 100) if total > 0 else 0

    print(f"\n{'=' * 50}")
    print(f"Comparison Results:")
    print(f"{'=' * 50}")
    print(f"Total files tested: {total}")
    print(f"✅ Correct detections: {correct_detections}")
    print(f"❌ False Positives: {false_positives} (detected code when there isn't)")
    print(f"❌ Miss Detects: {miss_detects} (didn't detect code when there is)")
    print(f"📊 Overall accuracy: {accuracy:.1f}%")

    # Display error details
    if false_positives > 0:
        print(f"\n🔴 False Positives:")
        for filename, result in detection_results.items():
            if result['detected'] and not result['manual_says_code']:
                print(f"  - {filename}")

    if miss_detects > 0:
        print(f"\n🔴 Miss Detects:")
        for filename, result in detection_results.items():
            if not result['detected'] and result['manual_says_code']:
                print(f"  - {filename} (type: {result['code_type']})")

    # Save detailed results
    with open('comparison_results.json', 'w') as f:
        json.dump(detection_results, f, indent=2)
    print(f"\n💾 Detailed results saved to comparison_results.json")


if __name__ == "__main__":
    print("Manual Validation Tool for Stack Overflow Files")
    print("=" * 50)

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--compare':
        compare_with_detection_results()
    else:
        manual_validation()
