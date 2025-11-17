import os
import pandas as pd
import numpy as np

from classifier.feature_extractor import extract_malicious_features
from .feature_extractor import PYTHON_SENSITIVE_APIS, C_SENSITIVE_APIS # This line will be added later

# --- Configuration: Define the target directories ---
BASE_DIR = 'data/'
DATA_FOLDERS = {
    'malicious_python': (os.path.join(BASE_DIR, 'malware_dataset/malicious_python'), 1, 'python'),
    'malicious_C': (os.path.join(BASE_DIR, 'malware_dataset/malicious_C'), 1, 'c'),
    'benign_python': (os.path.join(BASE_DIR, 'dataset_benign/benign_python'), 0, 'python'),
    'benign_C': (os.path.join(BASE_DIR, 'dataset_benign/benign_C'), 0, 'c'),
}

def build_initial_dataset():
    """
    Iterates over all source folders and reads file content.
    Assigns the correct label (0 or 1) and language.
    """
    all_data = []

    for key, (folder_path, label, language) in DATA_FOLDERS.items():
        print(f"Processing folder: {key} (Label: {label}, Language: {language})")
        
        # Walk through the folder path and find all .txt files
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Append initial data structure
                        all_data.append({
                            'content': content,
                            'label': label,
                            'language': language,
                            'filename': file_name
                        })
                        
                    except Exception as e:
                        print(f"Skipping file {file_path} due to error: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    print(f"\nInitial DataFrame created with {len(df)} entries.")
    
    return df

if __name__ == "__main__":
    # --- This part will be expanded in the next steps ---
    feature_df = build_initial_dataset()
    
    # Save the initial DataFrame for inspection
    # feature_df.to_csv('initial_dataset.csv', index=False)