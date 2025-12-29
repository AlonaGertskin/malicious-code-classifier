import os
import sys
import glob
import random
import re
import time
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# --- Path Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

# Define paths
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
PATHS = {
    "malicious_c": os.path.join(DATA_DIR, 'malware_dataset', 'malicious_C'),
    "malicious_py": os.path.join(DATA_DIR, 'malware_dataset', 'malicious_python'),
    "benign_c": os.path.join(DATA_DIR, 'benign', 'benign_C'),
    "benign_py": os.path.join(DATA_DIR, 'benign', 'benign_python'),
    "non_code": os.path.join(DATA_DIR, 'non_code')
}

REPORT_PATH = os.path.join(PROJECT_ROOT, 'pipeline_validation_report.txt')

# --- Imports ---
try:
    from extractor.code_detector import CodeDetector
except ImportError as e:
    print(f"[Critical Error] Failed to import 'extractor': {e}")
    sys.exit(1)

# --- Constants ---
LABEL_SAFE = 0
LABEL_MALICIOUS = 1
RANDOM_SEED = 42
MAX_FILE_SIZE = 500 * 1024  # 500KB Limit to prevent freezing on huge files

def read_file(filepath):
    """Reads file content, returns empty string if file is too big or unreadable."""
    try:
        # 1. Check size first
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            # print(f"    [Skipping] File too large: {os.path.basename(filepath)}")
            return ""
        
        # 2. Read content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def normalize_code(code_snippet):
    if not isinstance(code_snippet, str): return "" 
    code = re.sub(r'#.*', '', code_snippet) 
    code = re.sub(r'//.*', '', code) 
    return code.lower()

class LiveModel:
    def __init__(self, vectorizer, clf):
        self.vectorizer = vectorizer
        self.clf = clf

    def predict(self, content):
        clean_text = normalize_code(content)
        features = self.vectorizer.transform([clean_text])
        prediction = self.clf.predict(features)
        return prediction[0]

def collect_files(key_list, label_val, type_str):
    samples = []
    for key in key_list:
        files = glob.glob(os.path.join(PATHS[key], '*'))
        for f in files:
            if os.path.isfile(f):
                samples.append({
                    'path': f,
                    'label': label_val,
                    'type': type_str,
                    'lang': 'Python' if 'python' in key else 'C'
                })
    return samples

def prepare_balanced_test_environment():
    print("[*] 1. Collecting Data from all sources...")

    # 1. Collect Code Files
    mal_samples = collect_files(["malicious_c", "malicious_py"], LABEL_MALICIOUS, "malicious")
    ben_samples = collect_files(["benign_c", "benign_py"], LABEL_SAFE, "benign")
    
    # 2. Collect Non-Code Files
    non_code_paths = glob.glob(os.path.join(PATHS['non_code'], '*'))
    non_code_samples = [{'path': p, 'label': LABEL_SAFE, 'type': 'non_code', 'lang': 'None'} for p in non_code_paths]

    print(f"    - Found Malicious: {len(mal_samples)}")
    print(f"    - Found Benign:    {len(ben_samples)}")
    print(f"    - Found Non-Code:  {len(non_code_samples)}")

    # 3. Split Code Data (80% Train / 20% Test)
    mal_train, mal_test_pool = train_test_split(mal_samples, test_size=0.2, random_state=RANDOM_SEED)
    ben_train, ben_test_pool = train_test_split(ben_samples, test_size=0.2, random_state=RANDOM_SEED)
    
    # 4. Create Balanced Test Set
    min_count = min(len(mal_test_pool), len(ben_test_pool), len(non_code_samples))
    
    if min_count == 0:
        print("[!] Critical: Not enough files for testing. Proceeding with what is available.")
        min_count = 1

    print(f"[*] 2. Balancing Test Set (Limit: {min_count} per category)...")
    
    random.seed(RANDOM_SEED)
    final_test_mal = random.sample(mal_test_pool, min(len(mal_test_pool), min_count))
    final_test_ben = random.sample(ben_test_pool, min(len(ben_test_pool), min_count))
    final_test_nc  = random.sample(non_code_samples, min(len(non_code_samples), min_count))
    
    full_test_set = final_test_mal + final_test_ben + final_test_nc
    random.shuffle(full_test_set)
    
    # 5. Prepare Training Data (80% Mal + 80% Ben)
    full_train_set = mal_train + ben_train
    
    print(f"    -> Training Set Size: {len(full_train_set)} (Malicious & Benign)")
    print(f"    -> Testing Set Size:  {len(full_test_set)} (Balanced)")
    
    return full_train_set, full_test_set

def train_model_in_memory(train_data):
    print("[*] 3. Training Fresh Model (In-Memory)...")
    
    contents = []
    labels = []
    
    for item in train_data:
        text = read_file(item['path'])
        if text.strip():
            contents.append(normalize_code(text))
            labels.append(item['label'])
            
    print("    - Vectorizing...")
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), max_features=5000)
    X = vectorizer.fit_transform(contents)
    
    print("    - Fitting Random Forest...")
    clf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=RANDOM_SEED)
    clf.fit(X, labels)
    
    return LiveModel(vectorizer, clf)

def run_validation():
    # 1. Prepare
    train_set, test_set = prepare_balanced_test_environment()
    
    # 2. Train
    model = train_model_in_memory(train_set)
    
    # 3. Init Detector
    detector = CodeDetector(debug=False)
    
    # 4. Run Test
    print(f"\n[*] 4. Running Pipeline on {len(test_set)} files...")
    print("    (Skipping files > 500KB to prevent freezing)\n")
    
    stats = {
        "total": 0,
        "true_positive": 0,   
        "true_negative": 0,   
        "false_positive": 0,  
        "false_negative": 0, 

        "mal_missed_detector": 0,
        "mal_missed_classifier": 0,
        "ben_filtered": 0,
        "nc_filtered": 0,
        "nc_leaked_safe": 0,
        "ben_safe_model": 0
    }
    
    start_time = time.time()
    
    for i, item in enumerate(test_set):
        stats["total"] += 1
        
        # Debug print to catch hanging files
        # print(f"Checking [{i+1}]: {os.path.basename(item['path'])}", end='\r') 

        content = read_file(item['path'])
        
        # Skip if file was too big (content is empty)
        if not content:
            # Consider this a "Detector Filtered" event (too big to analyze)
            is_code = False
        else:
            try:
                blocks = detector.detect_code(content)
                is_code = len(blocks) > 0
            except:
                is_code = False
            
        final_prediction = LABEL_SAFE 
        
        if is_code:
            try:
                final_prediction = model.predict(content)
            except:
                final_prediction = LABEL_SAFE
        
        # Evaluation
        expected = item['label']
        is_malicious = (expected == LABEL_MALICIOUS)
        
        if is_malicious:
            if final_prediction == LABEL_MALICIOUS and is_code:
                stats["true_positive"] += 1
            else:
                stats["false_negative"] += 1 
                if not is_code: stats["mal_missed_detector"] += 1
                else: stats["mal_missed_classifier"] += 1     
        else:
            if final_prediction == LABEL_MALICIOUS and is_code:
                stats["false_positive"] += 1
            else:
                stats["true_negative"] += 1
                if not is_code:
                    if item['type'] == 'benign': stats['ben_filtered'] += 1
                    else: stats['nc_filtered'] += 1
                else:
                    if item['type'] == 'benign': stats['ben_safe_model'] += 1
                    elif item['type'] == 'non_code': stats['nc_leaked_safe'] += 1

        if (i+1) % 100 == 0:
             print(f"    Progress: {i+1}/{len(test_set)} files checked...")

    duration = time.time() - start_time
    
    # Report
    total = stats["total"]
    # Avoid div by zero
    if total == 0: total = 1
        
    fp_rate = (stats["false_positive"] / total) * 100
    fn_rate = (stats["false_negative"] / total) * 100
    acc = ((stats["true_positive"] + stats["true_negative"]) / total) * 100
    
    report = []
    report.append("========================================================")
    report.append("   MALICIOUS CODE CLASSIFIER - LIVE VALIDATION REPORT")
    report.append("========================================================")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Files Checked: {stats['total']}")
    report.append(f"Execution Time:      {duration:.2f}s")
    report.append("-" * 56)
    
    report.append(f"OVERALL ACCURACY:    {acc:.2f}%")
    report.append("-" * 56)
    
    report.append(f"FALSE POSITIVE RATE: {fp_rate:.2f}%  ({stats['false_positive']}/{total})")
    report.append(f"MISS DETECT RATE:    {fn_rate:.2f}%  ({stats['false_negative']}/{total})")
    report.append("-" * 56)
    
    report.append("DETAILED BREAKDOWN:")
    report.append(f"  * Malicious Caught:          {stats['true_positive']}")
    report.append(f"  * Malicious Missed (Det):    {stats['mal_missed_detector']}")
    report.append(f"  * Malicious Missed (Clf):    {stats['mal_missed_classifier']}")
    report.append(f"  * Benign Code Safe (Model):  {stats['ben_safe_model']}")
    report.append(f"  * Benign Code Filtered:      {stats['ben_filtered']} (Correct Rejection)")
    report.append(f"  * Non-Code Filtered:         {stats['nc_filtered']} (Correct Rejection)")
    report.append(f"  * Non-Code Leaked but Safe:  {stats['nc_leaked_safe']}")

    final_output = "\n".join(report)
    print("\n" + final_output)
    
    with open(REPORT_PATH, 'w') as f:
        f.write(final_output)
    print(f"\n[v] Report saved to: {REPORT_PATH}")

if __name__ == "__main__":
    run_validation()