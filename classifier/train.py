import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import dump
from pathlib import Path
from model import create_model 

# --- Config ---
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "code_dataset.csv"
MODEL_OUTPUT_PATH = BASE_DIR / "malicious_code_classifier.joblib"
VECTORIZER_OUTPUT_PATH = BASE_DIR / "code_vectorizer.joblib"
# NEW: Path for the text report
REPORT_OUTPUT_PATH = BASE_DIR / "training_results.txt"

def normalize_code(code_snippet):
    """
    Simple cleanup: remove comments and lowercase.
    """
    if not isinstance(code_snippet, str): return "" 
    # Remove Python style comments
    code = re.sub(r'#.*', '', code_snippet) 
    # Remove C style comments
    code = re.sub(r'//.*', '', code) 
    return code.lower()

def generate_report_string(y_true, y_pred, title):
    """
    Helper function that RETURNS a string report instead of printing it directly.
    """
    report_str = f"\n>>> {title} REPORT <<<\n"
    
    if len(y_true) == 0:
        report_str += "  (No samples in this category)\n"
        return report_str

    # Calculate Confusion Matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    acc = accuracy_score(y_true, y_pred)
    
    # Calculate percentages (safe division)
    fp_rate = (fp / (fp + tn)) * 100 if (fp + tn) > 0 else 0
    fn_rate = (fn / (fn + tp)) * 100 if (fn + tp) > 0 else 0
    
    report_str += f"  Total Samples: {len(y_true)}\n"
    report_str += f"  ACCURACY:      {acc * 100:.2f}%\n"
    report_str += f"  -----------------------------\n"
    report_str += f"  False Positives: {fp:<3} (Rate: {fp_rate:.2f}%) -> Benign flagged as Malicious (Bad!)\n"
    report_str += f"  Miss Detections: {fn:<3} (Rate: {fn_rate:.2f}%) -> Malicious missed (Dangerous!)\n"
    
    return report_str

def main():
    print("--- Starting Model Training & Evaluation ---")
    
    # 1. Loading Data
    if not DATASET_PATH.exists():
        print(f"Error: Dataset not found at {DATASET_PATH}")
        print("Please run 'build_dataset.py' first.")
        return
    
    df = pd.read_csv(DATASET_PATH).dropna(subset=['code'])
    
    X_raw = df['code']
    y = df['label']
    
    # Check if 'language' column exists
    if 'language' in df.columns:
        languages = df['language']
    else:
        print("Warning: 'language' column not found. Detailed language reports will be skipped.")
        languages = None

    # 2. Vectorizing
    print("Vectorizing code samples (learning keywords)...")
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), max_features=5000)
    X_features = vectorizer.fit_transform([normalize_code(c) for c in X_raw])

    # 3. Splitting Data (80% Train / 20% Test)
    print("Splitting data into Train (80%) and Test (20%)...")
    if languages is not None:
        X_train, X_test, y_train, y_test, lang_train, lang_test = train_test_split(
            X_features, y, languages, test_size=0.20, random_state=42, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X_features, y, test_size=0.20, random_state=42, stratify=y
        )

    # 4. Training
    print(f"Training model on {X_train.shape[0]} samples...")
    model = create_model()
    model.fit(X_train, y_train)
    print("Training complete.")
    
    # 5. Evaluation
    print("Running tests on unseen data...")
    y_pred = model.predict(X_test)

    # --- BUILD REPORT STRING ---
    full_report = ""
    full_report += "========================================\n"
    full_report += "   MALICIOUS CODE CLASSIFIER RESULTS    \n"
    full_report += "========================================\n"

    # 1. Overall Report
    full_report += generate_report_string(y_test, y_pred, "OVERALL (ALL LANGUAGES)")

    # 2. Language Specific Reports
    if languages is not None:
        # Python Only
        py_mask = (lang_test == 'python')
        full_report += generate_report_string(y_test[py_mask], y_pred[py_mask], "PYTHON ONLY")

        # C Only
        c_mask = (lang_test == 'c')
        full_report += generate_report_string(y_test[c_mask], y_pred[c_mask], "C LANGUAGE ONLY")
    
    # --- PRINT AND SAVE ---
    
    # Print to console
    print(full_report)
    
    # Save to file
    try:
        with open(REPORT_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(full_report)
        print(f"\n[SUCCESS] Detailed report saved to: {REPORT_OUTPUT_PATH}")
    except Exception as e:
        print(f"\n[ERROR] Could not save report to file: {e}")

    # 6. Save Model
    print(f"Saving model to {MODEL_OUTPUT_PATH}...")
    dump(model, MODEL_OUTPUT_PATH)
    dump(vectorizer, VECTORIZER_OUTPUT_PATH)
    print("Done.")

if __name__ == "__main__":
    main()
