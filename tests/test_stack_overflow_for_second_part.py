import requests
import json
import re
import html as html_module
import os
import sys
from pathlib import Path
from datetime import datetime

# -----------------------------------------------------------------
# THIS IS THE CHANGED SECTION (Lines 11-17)
# -----------------------------------------------------------------
# Get the directory where THIS script (test_stack_overflow.py) is
SCRIPT_DIR = Path(__file__).resolve().parent 
# Get the project's ROOT directory (one level up from 'tests/')
PROJECT_ROOT = SCRIPT_DIR.parent
# Define the output directory relative to the project root
BENIGN_DATA_DIR = PROJECT_ROOT / "data" / "benign"
# Define where to save the raw JSON backup (inside 'tests/')
RAW_JSON_DIR = SCRIPT_DIR
# -----------------------------------------------------------------


def get_stackoverflow_data(language="python", pagesize=5, filename=None):
    """Get Stack Overflow questions for specified language"""

    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "creation",
        "tagged": language,
        "site": "stackoverflow",
        "pagesize": pagesize,
        "filter": "withbody",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Stack Exchange: {e}")
        return []

    if 'items' not in data:
        print(f"Error: 'items' not in API response. Response: {data}")
        return []

    questions = []
    for item in data["items"]:
        question = {
            "title": item["title"],
            "body": item["body"],
            "question_id": item["question_id"],
        }
        questions.append(question)

    # Save the raw JSON file (optional, but good for backup)
    if filename is None:
        filename = f"stackoverflow_{language}_raw.json"
    
    # Ensure the 'tests' directory exists for the raw JSON
    RAW_JSON_DIR.mkdir(exist_ok=True)
    with open(RAW_JSON_DIR / filename, "w", encoding='utf-8') as f:
        json.dump(questions, f, indent=2)

    return questions

def extract_and_save_code(question_index=0, language="python", questions_data=[]):
    """
    Extracts clean code blocks from a Stack Overflow question
    and saves them to the benign dataset directory as .txt files.
    """
    
    # Check if index is valid
    if question_index >= len(questions_data):
        print(f"Error: Question index {question_index} out of range.")
        return 0, None

    # Get the specific question
    question = questions_data[question_index]
    title = html_module.unescape(question["title"])
    html_body = question["body"]

    # Extract the clean code blocks
    code_blocks = extract_expected_code_blocks(html_body)

    # If no code was found, skip
    if not code_blocks:
        return 0, None

    # Create a unique output filename
    safe_title = re.sub(r"[^a-zA-Z0-9_]", "_", title[:50]).lower()
    file_extension = ".txt" # As you requested
    output_filename = f"{language}_stackoverflow_{safe_title}_{question['question_id']}{file_extension}"
    
    # Ensure the output directory exists
    # This now uses the absolute path, so it will always work
    BENIGN_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    output_file_path = BENIGN_DATA_DIR / output_filename

    # Join all code blocks found in the post into one file
    full_code = "\n\n# --- New Code Block --- \n\n".join(code_blocks)

    # Save the clean code to the file
    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(full_code)
    except Exception as e:
        print(f"Error writing file {output_file_path}: {e}")
        return 0, None

    # Return the number of blocks and the path
    return len(code_blocks), str(output_file_path)

def create_all_code_files(language="python", questions_data=[]):
    """Creates clean code files for all downloaded questions."""
    
    if not questions_data:
        print(f"No questions data provided for {language}.")
        return
        
    print(f"Processing {len(questions_data)} questions for {language}...")
    
    files_created_count = 0
    for i, question in enumerate(questions_data):
        count, filepath = extract_and_save_code(i, language, questions_data)
        
        if count and (i + 1) % 25 == 0: # Print progress
             print(f"  ...processed {i+1}/{len(questions_data)} questions.")
        
        if count:
            files_created_count += 1
    
    print(f"Finished processing {language}. Created {files_created_count} code files.")

def extract_expected_code_blocks(html_body):
    """
    Extract the actual code blocks that Stack Overflow identified
    (This function is unchanged from your original)
    """
    code_pattern = r"<pre[^>]*><code[^>]*>(.*?)</code></pre>"
    code_blocks = re.findall(code_pattern, html_body, re.DOTALL)

    cleaned_blocks = []
    for block in code_blocks:
        clean_block = re.sub(r"<[^>]+>", "", block)
        clean_block = html_module.unescape(clean_block)
        clean_block = clean_block.strip()
        if clean_block:
            cleaned_blocks.append(clean_block)

    return cleaned_blocks

def main_collector(language, num_questions_to_fetch):
    """
    Main function to collect data for a specific language.
    """
    print(f"--- Collecting data for: {language.upper()} ---")
    print(f"Files will be saved to: {BENIGN_DATA_DIR}")
    
    all_questions = []
    max_per_page = 100
    pages_to_fetch = (num_questions_to_fetch + max_per_page - 1) // max_per_page
    
    print(f"Fetching {num_questions_to_fetch} questions over {pages_to_fetch} API call(s)...")
    
    remaining_questions = num_questions_to_fetch
    
    for i in range(pages_to_fetch):
        current_page_size = min(remaining_questions, max_per_page)
        if current_page_size <= 0:
            break
            
        print(f"Fetching page {i+1}/{pages_to_fetch} ({current_page_size} questions)...")
        
        questions = get_stackoverflow_data(language, pagesize=current_page_size)
        all_questions.extend(questions)
        
        remaining_questions -= current_page_size

    print(f"Total questions downloaded for {language}: {len(all_questions)}")
    
    create_all_code_files(language, all_questions)
    print(f"--- Finished collecting for: {language.upper()} ---")

if __name__ == "__main__":
    
    # -----------------------------------------------------------------
    # CHANGE THIS VARIABLE to download more/fewer questions
    # -----------------------------------------------------------------
    NUM_TO_FETCH_PER_LANG = 100  # e.g., set to 1000 to get 1000 questions
    # -----------------------------------------------------------------

    if len(sys.argv) > 1 and sys.argv[1] in ['python', 'c']:
        lang = sys.argv[1]
        main_collector(language=lang, num_questions_to_fetch=NUM_TO_FETCH_PER_LANG)
    else:
        print("Starting data collection for BOTH Python and C.")
        
        main_collector(language="python", num_questions_to_fetch=NUM_TO_FETCH_PER_LANG)
        print("\n" + "="*30 + "\n")
        main_collector(language="c", num_questions_to_fetch=NUM_TO_FETCH_PER_LANG)

    print(f"\nAll tasks complete. Check the '{BENIGN_DATA_DIR}' directory.")