import requests
import json
import re
from extractor.code_detector import CodeDetector
import html as html_module
# run with python -m tests.test_stack_overflow in command line

def get_simple_stackoverflow_data(language='python', pagesize=5):
    """Get Stack Overflow questions for specified language"""
    
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        'order': 'desc',
        'sort': 'votes',    
        'tagged': language,
        'site': 'stackoverflow',
        'pagesize': pagesize,
        'filter': 'withbody'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    questions = []
    for item in data['items']:
        question = {
            'title': item['title'],
            'body': item['body'],
            'question_id': item['question_id']
        }
        questions.append(question)
    
    filename = f'simple_stackoverflow_{language}_test.json'
    with open(filename, 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"Saved {len(questions)} {language} questions to {filename}")
    return questions

def extract_test_case(question_index=0, language='python'):
    """Extract a clean test case from the Stack Overflow data"""
    
    # Load the data for the specified language
    filename = f'simple_stackoverflow_{language}_test.json'
    with open(filename, 'r') as f:
        questions = json.load(f)

    # Take the specified question
    question = questions[question_index]
    title = html_module.unescape(question['title'])
    html_body = question['body']

    # Simple function to remove HTML tags and extract text
    def clean_html(html):
        text = re.sub(r'<[^>]+>', '', html)
        text = html_module.unescape(text)
        return text

    # Extract code blocks
    code_blocks = re.findall(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', html_body, re.DOTALL)
    clean_text = clean_html(html_body)

    # Create test content
    test_content = f"""Question: {title}

{clean_text}

Expected code blocks found: {len(code_blocks)}
"""

    # Create output filename
    safe_title = re.sub(r'[^a-zA-Z0-9_]', '_', title[:30]).lower()
    output_file = f'tests/test_samples/{language}_stackoverflow_{safe_title}.txt'

    # Save the test case
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"Saved {language} test case to: {output_file}")
    print(f"Expected to find: {len(code_blocks)} code blocks")
    return len(code_blocks)

def create_all_tests(language='python'):
    """Create test files for all downloaded questions"""
    filename = f'simple_stackoverflow_{language}_test.json'
    with open(filename, 'r') as f:
        questions = json.load(f)
    
    for i, question in enumerate(questions):
        print(f"\n--- {language.upper()} Question {i+1}: {question['title'][:50]}... ---")
        extract_test_case(i, language)

def test_both_languages():
    """Test both C and Python"""
    
    # Get C questions
    print("=== GETTING C QUESTIONS ===")
    get_simple_stackoverflow_data('c', 1)
    create_all_tests('c')
    
    print("\n=== GETTING PYTHON QUESTIONS ===")
    get_simple_stackoverflow_data('python', 0)
    create_all_tests('python')

if __name__ == "__main__":
    test_both_languages()