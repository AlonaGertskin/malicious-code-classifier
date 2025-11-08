import os
import pandas as pd
import random
from pathlib import Path

# --- Path Definitions ---
# This script sits in the project root, so we can define paths from here
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
BENIGN_DIR = DATA_DIR / "benign"
MALICIOUS_DIR = DATA_DIR / "malicious"
CLASSIFIER_DIR = PROJECT_ROOT / "classifier"
OUTPUT_CSV_PATH = CLASSIFIER_DIR / "code_dataset.csv"

def load_code_from_directory(directory, label):
    """
    Loads all .txt files from a directory, reads their content,
    and assigns a label.
    """
    code_samples = []
    # Use rglob to find all .txt files in all subfolders
    for file_path in directory.rglob('*.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
                if code.strip(): # Ensure the file is not empty
                    code_samples.append({'code': code, 'label': label})
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            
    return code_samples

def main():
    print("--- Starting Dataset Builder ---")
    
    # 1. Check if data directories exist
    if not BENIGN_DIR.exists():
        print(f"!!! ERROR: Benign directory not found at: {BENIGN_DIR}")
        print("Please make sure you have run the 'test_stack_overflow.py' script to collect benign data.")
        return

    if not MALICIOUS_DIR.exists():
        print(f"!!! ERROR: Malicious directory not found at: {MALICIOUS_DIR}")
        print("Please create this folder and fill it with malicious .txt code samples.")
        return

    # 2. Load Benign (Label 0)
    print(f"Loading benign code (Label 0) from: {BENIGN_DIR}...")
    benign_samples = load_code_from_directory(BENIGN_DIR, 0)
    print(f"Found {len(benign_samples)} benign samples.")

    # 3. Load Malicious (Label 1)
    print(f"Loading malicious code (Label 1) from: {MALICIOUS_DIR}...")
    malicious_samples = load_code_from_directory(MALICIOUS_DIR, 1)
    print(f"Found {len(malicious_samples)} malicious samples.")

    # 4. Check if we have data to work with
    if len(benign_samples) == 0 or len(malicious_samples) == 0:
        print("!!! ERROR: Not enough data. Both benign and malicious folders must contain .txt files.")
        return

    # 5. Combine and Shuffle
    print("Combining and shuffling all samples...")
    all_samples = benign_samples + malicious_samples
    random.shuffle(all_samples) # This is critical for training
    
    # 6. Create DataFrame
    df = pd.DataFrame(all_samples)
    
    # 7. Create output directory (classifier/) if it doesn't exist
    CLASSIFIER_DIR.mkdir(exist_ok=True)
    
    # 8. Save to CSV
    try:
        df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        print("\n--- SUCCESS! ---")
        print(f"Dataset saved to: {OUTPUT_CSV_PATH}")
        print(f"Total samples: {len(df)}")
        print(f" - Benign: {len(benign_samples)}")
        print(f" - Malicious: {len(malicious_samples)}")
        print("\nYou are now ready to run 'classifier/train.py'")
    except Exception as e:
        print(f"!!! ERROR: Failed to save CSV file: {e}")

if __name__ == "__main__":
    main()