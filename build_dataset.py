import os
import pandas as pd
import random
from pathlib import Path

# --- Path Definitions ---
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

# Benign Paths (Benign code directories)
BENIGN_PARENT_DIR = DATA_DIR / "benign"
BENIGN_C_DIR = BENIGN_PARENT_DIR / "benign_C"
BENIGN_PYTHON_DIR = BENIGN_PARENT_DIR / "benign_python"

# Malicious Paths (Malicious code directories)
MALWARE_DATASET_DIR = DATA_DIR / "malware_dataset"
MALICIOUS_C_DIR = MALWARE_DATASET_DIR / "malicious_C"
MALICIOUS_PYTHON_DIR = MALWARE_DATASET_DIR / "malicious_python"

# Output Path
CLASSIFIER_DIR = PROJECT_ROOT / "classifier"
OUTPUT_CSV_PATH = CLASSIFIER_DIR / "code_dataset.csv"

def load_code_from_directory(directory, label, language_tag):
    """
    Loads files from a directory and tags them with both label and language.
    """
    code_samples = []
    
    # Check if directory exists
    if not directory.exists():
        print(f"Warning: Directory not found: {directory}")
        return []
        
    # Search for all .txt files in the directory
    for file_path in directory.rglob('*.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
                # If the file is not empty, add it to the list
                if code.strip():
                    code_samples.append({
                        'code': code, 
                        'label': label, 
                        'language': language_tag
                    })
        except Exception as e:
            # Ignore read errors in individual files
            pass
            
    return code_samples

def main():
    print("--- Starting Dataset Builder ---")
    
    # 1. Loading Benign code
    print("Loading Benign C files...")
    benign_c = load_code_from_directory(BENIGN_C_DIR, 0, 'c')
    print(f"Found {len(benign_c)} benign C files.")

    print("Loading Benign Python files...")
    benign_py = load_code_from_directory(BENIGN_PYTHON_DIR, 0, 'python')
    print(f"Found {len(benign_py)} benign Python files.")
    
    # 2. Loading Malicious code
    print("Loading Malicious C files...")
    mal_c = load_code_from_directory(MALICIOUS_C_DIR, 1, 'c')
    print(f"Found {len(mal_c)} malicious C files.")

    print("Loading Malicious Python files...")
    mal_py = load_code_from_directory(MALICIOUS_PYTHON_DIR, 1, 'python')
    print(f"Found {len(mal_py)} malicious Python files.")

    # 3. Combine and shuffle data
    all_samples = benign_c + benign_py + mal_c + mal_py
    random.shuffle(all_samples)
    
    if not all_samples:
        print("!!! ERROR: No data found. Please check your directories and run the collection scripts.")
        return

    # 4. Create DataFrame and save to CSV
    df = pd.DataFrame(all_samples)
    
    # Create output directory if it doesn't exist
    CLASSIFIER_DIR.mkdir(exist_ok=True)
    
    try:
        df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        
        print("\n--- DATASET CREATED SUCCESSFULLY ---")
        print(f"Total samples in CSV: {len(df)}")
        print(f"Breakdown:")
        print(f" - Benign Python: {len(benign_py)}")
        print(f" - Benign C:      {len(benign_c)}")
        print(f" - Malicious Python: {len(mal_py)}")
        print(f" - Malicious C:      {len(mal_c)}")
        print(f"\nSaved to: {OUTPUT_CSV_PATH}")
        print("You are now ready to run 'python classifier/train.py'")
        
    except Exception as e:
        print(f"!!! ERROR: Failed to save CSV file: {e}")

if __name__ == "__main__":
    main()
