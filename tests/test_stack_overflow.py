import requests
import json
import re
from extractor.code_detector import CodeDetector
import html as html_module
from datetime import datetime
import os

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

    print(f"Saved {len(questions)} {language} questions to {filename}")
    return questions

def extract_test_case(question_index=0, language="python", filename=None):
    """Extract a clean test case from the Stack Overflow data"""

    # Load the data for the specified language
    if filename is None:
        filename = f"stackoverflow_{language}_test.json"
    try:
        with open(filename, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(
            f"Error: File '{filename}' not found. Run get_stackoverflow_data() first."
        )
        return None, None

        # Check if question index is valid
    if question_index >= len(questions):
        print(
            f"Error: Question index {question_index} out of range. Available: 0-{len(questions)-1}"
        )
        return None, None

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

Expected code blocks found: {len(code_blocks)}
"""

    # Create output filename
    safe_title = re.sub(r"[^a-zA-Z0-9_]", "_", title[:30]).lower()
    output_file = f"tests/test_samples/{language}_stackoverflow_{safe_title}.txt"

    # Save the test case
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    print(f"Saved {language} test case to: {output_file}")
    print(f"Expected to find: {len(code_blocks)} code blocks")
    return len(code_blocks), code_blocks

def create_all_tests(language="python", filename=None):
    """Create test files for all downloaded questions"""

    # Use provided filename or create the standard one
    if filename is None:
        filename = f"stackoverflow_{language}_test.json"

    try:
        with open(filename, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(
            f"Error: File '{filename}' not found. Run get_stackoverflow_data() first."
        )
        return

    print(
        f"Creating test files for {len(questions)} {language} questions from {filename}"
    )

    for i, question in enumerate(questions):
        print(
            f"\n--- {language.upper()} Question {i+1}: {question['title'][:50]}... ---"
        )
        count, blocks = extract_test_case(i, language, filename)

        if count is not None:
            print(f"    Created test file with {count} expected code blocks")
        else:
            print(f"    Error creating test file for question {i+1}")

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

    """Test both C and Python"""

    # Get C questions
    print("=== GETTING C QUESTIONS ===")
    get_stackoverflow_data("c", 1)
    create_all_tests("c")

    print("\n=== GETTING PYTHON QUESTIONS ===")
    get_stackoverflow_data("python", 0)
    create_all_tests("python")


def test_both_languages():
    # Get C questions FIRST, then create tests
    get_stackoverflow_data("c", 3)  # Download C questions
    create_all_tests("c")           # Create test files from downloaded data

    # Get Python questions FIRST, then create tests  
    get_stackoverflow_data("python", 3)  # Download Python questions
    create_all_tests("python")           # Create test files from downloaded data

if __name__ == "__main__":
    test_both_languages()
