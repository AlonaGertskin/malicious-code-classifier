import requests
import json
import re
from extractor.code_detector import CodeDetector
import html as html_module
from datetime import datetime
import os
from tests.test_detector import test_all_sample_files, run_file_test

# run with python -m tests.test_stack_overflow in command line

def get_stackoverflow_data(language="python", pagesize=5, filename=None):
    """Get Stack Overflow questions for specified language"""

    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "votes",
        "tagged": language,
        "site": "stackoverflow",
        "pagesize": pagesize,
        "filter": "withbody",
    }

    response = requests.get(url, params=params)
    data = response.json()

    questions = []
    for item in data["items"]:
        question = {
            "title": item["title"],
            "body": item["body"],
            "question_id": item["question_id"],
        }
        questions.append(question)

    # Use provided filename or create a standard one
    if filename is None:
        filename = f"stackoverflow_{language}_test.json"
    with open(filename, "w") as f:
        json.dump(questions, f, indent=2)

    return questions

def extract_test_case(question_index=0, language="python"):
    """Extract a clean test case from the Stack Overflow data"""

    # Load the data for the specified language
    filename = f"stackoverflow_{language}_test.json"
    
    try:
        with open(filename, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(
            f"Error: File '{filename}' not found. Run get_stackoverflow_data() first."
        )
        return None, None, None

        # Check if question index is valid
    if question_index >= len(questions):
        print(
            f"Error: Question index {question_index} out of range. Available: 0-{len(questions)-1}"
        )
        return None, None, None

    # Take the specified question
    question = questions[question_index]
    title = html_module.unescape(question["title"])
    html_body = question["body"]

    # Simple function to remove HTML tags and extract text
    def clean_html(html):
        text = re.sub(r"<[^>]+>", "", html)
        text = html_module.unescape(text)
        return text

    # Extract code blocks
    code_blocks = extract_expected_code_blocks(html_body)

    clean_text = clean_html(html_body)

    # Create test content
    test_content = f"""Question: {title}

{clean_text}

"""

    # Create output filename
    safe_title = re.sub(r"[^a-zA-Z0-9_]", "_", title[:30]).lower()
    output_file = f"tests/test_samples/{language}_stackoverflow_{safe_title}.txt"

    # Save the test case
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    return len(code_blocks), code_blocks, output_file

def create_all_tests(language="python"):
    """Create test files for all downloaded questions"""

    filename = f"stackoverflow_{language}_test.json"

    try:
        with open(filename, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(
            f"Error: File '{filename}' not found. Run get_stackoverflow_data() first."
        )
        return {}
    
    expected_blocks_dict = {}

    for i, question in enumerate(questions):
        count, blocks, test_filename = extract_test_case(i, language)
        
        if count is None:
            print(f"    Error creating test file for question {i+1}")
        else:
            expected_blocks_dict[os.path.basename(test_filename)] = blocks
    
    return expected_blocks_dict 

def extract_expected_code_blocks(html_body):
    """
    Extract the actual code blocks that Stack Overflow identified
    This gives us the 'ground truth' to compare against
    """
    # Find all code blocks in <pre><code> tags
    code_pattern = r"<pre[^>]*><code[^>]*>(.*?)</code></pre>"
    code_blocks = re.findall(code_pattern, html_body, re.DOTALL)

    # Clean HTML entities and tags from code blocks
    cleaned_blocks = []
    for block in code_blocks:
        # Remove HTML tags within code
        clean_block = re.sub(r"<[^>]+>", "", block)
        # Decode HTML entities
        clean_block = html_module.unescape(clean_block)
        # Remove extra whitespace but preserve structure
        clean_block = clean_block.strip()
        if clean_block:  # Only add non-empty blocks
            cleaned_blocks.append(clean_block)

    return cleaned_blocks

def test_both_languages():
    # Get C questions FIRST, then create tests
    get_stackoverflow_data("c", 3)  # Download C questions
    expected_blocks_c = create_all_tests("c")           # Create test files from downloaded data

    # Get Python questions FIRST, then create tests  
    get_stackoverflow_data("python", 3)  # Download Python questions
    expected_blocks_python = create_all_tests("python")           # Create test files from downloaded data

def stack_overflow_testing():
    """
    Complete Stack Overflow testing pipeline:
    1. Download questions
    2. Create test files
    3. Run CodeDetector
    4. Compare with expected results
    5. Generate detailed validation report
    """
    
    print("=== STACK OVERFLOW TESTING ===")
    
    # Step 1 & 2: Get questions and create test files (returns expected blocks)
    print("\n1. Getting C questions and creating test files...")
    get_stackoverflow_data("c", 3)
    expected_blocks_c = create_all_tests("c")
    
    print("\n2. Getting Python questions and creating test files...")
    get_stackoverflow_data("python", 3)
    expected_blocks_python = create_all_tests("python")
    
    # Combine expected blocks
    all_expected_blocks = {**expected_blocks_c, **expected_blocks_python}
    
    print(f"\n3. Created {len(all_expected_blocks)} test files with expected blocks")
    
    # Step 3: Run CodeDetector on all Stack Overflow test files
    print("\n4. Running CodeDetector on Stack Overflow test files...")
    stackoverflow_files = [f for f in os.listdir("tests/test_samples/") 
                          if "stackoverflow" in f and f.endswith(".txt")]
    
    detection_results = {}
    for filename in stackoverflow_files:
        filepath = f"tests/test_samples/{filename}"
        detected_blocks, file_result = run_file_test(filepath)
        detection_results[filename] = detected_blocks
    
    # Step 4: Compare expected vs detected
    print("\n5. Validating results...")
    validation_results = validate_detection_results(all_expected_blocks, detection_results)
    
    # Step 5: Generate detailed report
    print("\n6. Generating validation report...")
    save_validation_report(validation_results)
    
    return validation_results

def validate_detection_results(expected_blocks_dict, detection_results):
    """
    Compare expected vs detected blocks line by line
    
    Args:
        expected_blocks_dict: {filename: [code_blocks]} from create_all_tests
        detection_results: {filename: detected_blocks} from run_file_test
    
    Returns:
        validation_results: Detailed comparison data
    """
    validation_results = {
        'files': {},
        'statistics': {
            'total_files': 0,
            'correct_files': 0,
            'total_expected_lines': 0,
            'total_detected_lines': 0,
            'correct_lines': 0,
            'false_positives': 0,
            'missed_detections': 0
        }
    }
    
    for filename in expected_blocks_dict.keys():
        if filename not in detection_results:
            print(f"Warning: No detection results for {filename}")
            continue
        
        expected_blocks = expected_blocks_dict[filename]
        detected_blocks = detection_results[filename]
        
        # Convert to line-by-line comparison
        expected_lines = []
        for block in expected_blocks:
            expected_lines.extend(block.split('\n'))
        expected_lines = [line.strip() for line in expected_lines if line.strip()]
        
        detected_lines = []
        for block in detected_blocks:
            if 'content' in block:
                detected_lines.extend(block['content'])
        detected_lines = [line.strip() for line in detected_lines if line.strip()]
        
        # Line-by-line comparison
        file_result = compare_lines(expected_lines, detected_lines, filename)
        validation_results['files'][filename] = file_result
        
        # Update statistics
        stats = validation_results['statistics']
        stats['total_files'] += 1
        stats['total_expected_lines'] += len(expected_lines)
        stats['total_detected_lines'] += len(detected_lines)
        stats['correct_lines'] += file_result['correct_lines']
        stats['false_positives'] += file_result['false_positives']
        stats['missed_detections'] += file_result['missed_detections']
        
        # Check if entire file is correct
        if file_result['missed_detections'] == 0 and file_result['false_positives'] == 0:
            stats['correct_files'] += 1
    
    return validation_results

def compare_lines(expected_lines, detected_lines, filename):
    """
    Line-by-line comparison with context
    
    Returns:
        dict with detailed comparison results
    """
    result = {
        'filename': filename,
        'expected_count': len(expected_lines),
        'detected_count': len(detected_lines),
        'correct_lines': 0,
        'false_positives': 0,
        'missed_detections': 0,
        'false_positive_details': [],  # Lines detected but shouldn't be
        'missed_detection_details': []  # Lines that should be detected but weren't
    }
    
    # Find correct matches
    matched_expected = set()
    matched_detected = set()
    
    for i, expected_line in enumerate(expected_lines):
        for j, detected_line in enumerate(detected_lines):
            if j in matched_detected:
                continue
            if lines_match(expected_line, detected_line):
                result['correct_lines'] += 1
                matched_expected.add(i)
                matched_detected.add(j)
                break
    
    # Find false positives (detected but not expected)
    for j, detected_line in enumerate(detected_lines):
        if j not in matched_detected:
            result['false_positives'] += 1
            context = get_line_context(detected_lines, j)
            result['false_positive_details'].append({
                'line': detected_line,
                'line_number': j + 1,
                'context': context
            })
    
    # Find missed detections (expected but not detected)
    for i, expected_line in enumerate(expected_lines):
        if i not in matched_expected:
            result['missed_detections'] += 1
            context = get_line_context(expected_lines, i)
            result['missed_detection_details'].append({
                'line': expected_line,
                'expected_line_number': i + 1,
                'context': context
            })
    
    return result

def lines_match(expected, detected):
    """
    Check if two lines match exactly
    """
    return expected.strip() == detected.strip()

def get_line_context(lines, index):
    """
    Get context lines around a specific line
    """
    context = {
        'before': lines[index - 1] if index > 0 else None,
        'after': lines[index + 1] if index < len(lines) - 1 else None
    }
    return context

def save_validation_report(validation_results):
    """
    Save comprehensive validation report
    """
    from datetime import datetime
    
    output_file = "stackoverflow_validation.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Stack Overflow Validation Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Overall statistics
        stats = validation_results['statistics']
        total_files = stats['total_files']
        correct_files = stats['correct_files']
        total_expected = stats['total_expected_lines']
        total_detected = stats['total_detected_lines']
        correct_lines = stats['correct_lines']
        false_positives = stats['false_positives']
        missed_detections = stats['missed_detections']
        
        false_positive_rate = false_positives / total_detected if total_detected > 0 else 0
        missed_detection_rate = missed_detections / total_expected if total_expected > 0 else 0
        detection_rate = correct_lines / total_expected if total_expected > 0 else 0
        file_accuracy = correct_files / total_files if total_files > 0 else 0
        
        f.write("OVERALL STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total files tested: {total_files}\n")
        f.write(f"Files completely correct: {correct_files} ({file_accuracy:.1%})\n")
        f.write(f"Total expected lines: {total_expected}\n")
        f.write(f"Total detected lines: {total_detected}\n")
        f.write(f"Correct lines: {correct_lines}\n")
        f.write(f"Detection rate: {detection_rate:.1%}\n")
        f.write(f"False positives: {false_positives} ({false_positive_rate:.1%})\n")
        f.write(f"Missed detections: {missed_detections} ({missed_detection_rate:.1%})\n\n")
        
        # Detailed file-by-file results
        f.write("DETAILED FILE RESULTS\n")
        f.write("-" * 40 + "\n\n")
        
        for filename, file_result in validation_results['files'].items():
            f.write(f"File: {filename}\n")
            f.write(f"Expected lines: {file_result['expected_count']}\n")
            f.write(f"Detected lines: {file_result['detected_count']}\n")
            f.write(f"Correct: {file_result['correct_lines']}\n")
            f.write(f"False positives: {file_result['false_positives']}\n")
            f.write(f"Missed detections: {file_result['missed_detections']}\n")
            
            # False positives details
            if file_result['false_positive_details']:
                f.write("\nFALSE POSITIVES (detected but shouldn't be):\n")
                for fp in file_result['false_positive_details']:
                    f.write(f"  Line {fp['line_number']}: {fp['line']}\n")
                    if fp['context']['before']:
                        f.write(f"    Before: {fp['context']['before']}\n")
                    if fp['context']['after']:
                        f.write(f"    After: {fp['context']['after']}\n")
            
            # Missed detections details
            if file_result['missed_detection_details']:
                f.write("\nMISSED DETECTIONS (should be detected but weren't):\n")
                for md in file_result['missed_detection_details']:
                    f.write(f"  Expected line {md['expected_line_number']}: {md['line']}\n")
                    if md['context']['before']:
                        f.write(f"    Before: {md['context']['before']}\n")
                    if md['context']['after']:
                        f.write(f"    After: {md['context']['after']}\n")
            
            f.write("\n" + "-" * 60 + "\n\n")
    
    print(f"Validation report saved to {output_file}")
    
    # Print summary to console
    stats = validation_results['statistics']
    false_positive_rate = stats['false_positives'] / stats['total_detected_lines'] if stats['total_detected_lines'] > 0 else 0
    missed_detection_rate = stats['missed_detections'] / stats['total_expected_lines'] if stats['total_expected_lines'] > 0 else 0
    detection_rate = stats['correct_lines'] / stats['total_expected_lines'] if stats['total_expected_lines'] > 0 else 0
    file_accuracy = stats['correct_files'] / stats['total_files'] if stats['total_files'] > 0 else 0
    
    print(f"\nVALIDATION SUMMARY:")
    print(f"Detection Rate: {detection_rate:.1%}")
    print(f"File Accuracy: {file_accuracy:.1%}")
    print(f"False Positives: {stats['false_positives']} ({false_positive_rate:.1%})")
    print(f"Missed Detections: {stats['missed_detections']} ({missed_detection_rate:.1%})")

if __name__ == "__main__":
    stack_overflow_testing()


# if __name__ == "__main__":
#     test_both_languages()
