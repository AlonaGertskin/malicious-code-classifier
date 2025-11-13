import os
import pandas as pd
import random
from pathlib import Path

# --- Path Definitions ---
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

# --- UPDATED Benign Paths ---
BENIGN_PARENT_DIR = DATA_DIR / "benign"
BENIGN_C_DIR = BENIGN_PARENT_DIR / "benign_C"
BENIGN_PYTHON_DIR = BENIGN_PARENT_DIR / "benign_python"
# -------------------------

# --- Malicious Paths (these are correct) ---
MALWARE_DATASET_DIR = DATA_DIR / "malware_dataset"
MALICIOUS_C_DIR = MALWARE_DATASET_DIR / "malicious_C"
MALICIOUS_PYTHON_DIR = MALWARE_DATASET_DIR / "malicious_python"
# -------------------------

CLASSIFIER_DIR = PROJECT_ROOT / "classifier"
OUTPUT_CSV_PATH = CLASSIFIER_DIR / "code_dataset.csv"

def load_code_from_directory(directory, label):
    """
    Loads all .txt files from a directory (and its subfolders),
    reads their content, and assigns a label.
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
    if not BENIGN_C_DIR.exists() or not BENIGN_PYTHON_DIR.exists():
        print(f"!!! ERROR: Benign directories not found.")
        print(f"Please check that these folders exist:")
        print(f" - {BENIGN_C_DIR}")
        print(f" - {BENIGN_PYTHON_DIR}")
        return

    if not MALICIOUS_C_DIR.exists() or not MALICIOUS_PYTHON_DIR.exists():
        print(f"!!! ERROR: Malicious directories not found.")
        print(f"Please check that these folders exist:")
        print(f" - {MALICIOUS_C_DIR}")
        print(f" - {MALICIOUS_PYTHON_DIR}")
        return

    # 2. Load Benign (Label 0)
    print(f"Loading benign C code (Label 0) from: {BENIGN_C_DIR}...")
    benign_c_samples = load_code_from_directory(BENIGN_C_DIR, 0)
    print(f"Found {len(benign_c_samples)} benign C samples.")

    print(f"Loading benign Python code (Label 0) from: {BENIGN_PYTHON_DIR}...")
    benign_python_samples = load_code_from_directory(BENIGN_PYTHON_DIR, 0)
    print(f"Found {len(benign_python_samples)} benign Python samples.")

    total_benign = len(benign_c_samples) + len(benign_python_samples)
    print(f"--- Total benign samples found: {total_benign} ---")

    # 3. Load Malicious (Label 1)
    print(f"Loading malicious C code (Label 1) from: {MALICIOUS_C_DIR}...")
    malicious_c_samples = load_code_from_directory(MALICIOUS_C_DIR, 1)
    print(f"Found {len(malicious_c_samples)} malicious C samples.")
    
    print(f"Loading malicious Python code (Label 1) from: {MALICIOUS_PYTHON_DIR}...")
    malicious_python_samples = load_code_from_directory(MALICIOUS_PYTHON_DIR, 1)
    print(f"Found {len(malicious_python_samples)} malicious Python samples.")

    total_malicious = len(malicious_c_samples) + len(malicious_python_samples)
    print(f"--- Total malicious samples found: {total_malicious} ---")

    # 4. Check if we have data to work with
    if total_benign == 0 or total_malicious == 0:
        print("!!! ERROR: Not enough data. All data folders must contain .txt files.")
        return

    # 5. Combine and Shuffle
    print("Combining and shuffling all samples...")
    all_samples = (
        benign_c_samples + 
        benign_python_samples + 
        malicious_c_samples + 
        malicious_python_samples
    )
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
        print(f" - Benign: {total_benign}")
        print(f" - Malicious: {total_malicious}")
        print("\nYou are now ready to run 'classifier/train.py'")
    except Exception as e:
        print(f"!!! ERROR: Failed to save CSV file: {e}")

if __name__ == "__main__":
    main()
