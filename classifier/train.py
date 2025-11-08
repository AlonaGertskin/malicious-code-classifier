import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump
from pathlib import Path

# Import the model function from your other file
from model import create_model 

# --- File Paths ---
# This makes the paths work from anywhere
BASE_DIR = Path(__file__).resolve().parent # The classifier/ folder
DATASET_PATH = BASE_DIR / "code_dataset.csv" # The file your build_dataset.py will create
MODEL_OUTPUT_PATH = BASE_DIR / "malicious_code_classifier.joblib"
VECTORIZER_OUTPUT_PATH = BASE_DIR / "code_vectorizer.joblib"

def normalize_code(code_snippet):
    """
    A simple function to clean and normalize code before vectorization.
    """
    if not isinstance(code_snippet, str):
        return "" # Handle empty or non-string data
    
    # Simple normalization: lowercasing and removing comments
    code = re.sub(r'#.*', '', code_snippet) # Remove python-style comments
    code = re.sub(r'//.*', '', code) # Remove C-style comments
    return code.lower()

def load_data(path):
    """
    Loads the dataset from the specified CSV file.
    """
    print(f"Loading dataset from: {path}")
    if not path.exists():
        print(f"!!! ERROR: Dataset file not found at {path}")
        print("Please run the data collection and build_dataset.py scripts first.")
        return None
    
    try:
        df = pd.read_csv(path)
        if 'code' not in df.columns or 'label' not in df.columns:
            print("!!! ERROR: Dataset CSV must have 'code' and 'label' columns.")
            return None
        
        # Drop rows where 'code' is missing
        df = df.dropna(subset=['code'])
        print(f"Dataset loaded successfully: {len(df)} samples.")
        return df
    except Exception as e:
        print(f"!!! ERROR: Failed to load dataset: {e}")
        return None

def main():
    print("--- Starting Model Training Script ---")
    
    # 1. Load Data
    df = load_data(DATASET_PATH)
    if df is None:
        return # Stop if data loading failed

    X_raw = df['code'] # The code text
    y = df['label']    # The 0 (benign) or 1 (malicious)

    # 2. Preprocess & Feature Extraction (TF-IDF)
    # We must turn raw code text into numbers (vectors)
    print("Normalizing code samples...")
    X_normalized = [normalize_code(code) for code in X_raw]
    
    print("Initializing TF-IDF Vectorizer...")
    # TF-IDF finds the most "important" words in the code
    # (e.g., "socket" and "os.dup2" might be very important)
    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2), # Looks at single words AND pairs of words
        max_features=5000,  # Limit to the top 5000 most important words/pairs
    )
    
    print("Extracting features (fit_transform)...")
    X_features = vectorizer.fit_transform(X_normalized)
    print(f"Feature matrix created with shape: {X_features.shape}")

    # 3. Split Data
    print("Splitting data into train and test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_features,
        y,
        test_size=0.20, # 20% for testing, 80% for training
        random_state=42,
        stratify=y # Ensures both train and test sets have a similar mix of 0s and 1s
    )
    print(f"Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")

    # 4. Create and Train Model
    print("Creating model (from model.py)...")
    model = create_model()
    
    print("Training model...")
    model.fit(X_train, y_train)
    print("Training complete.")

    # 5. Evaluate Model
    print("Evaluating model on test set...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test, 
        y_pred, 
        target_names=['Benign (0)', 'Malicious (1)']
    )

    print("\n--- MODEL EVALUATION RESULTS ---")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(report)
    print("--------------------------------")

    # 6. Save Model and Vectorizer for later use
    print("Saving trained model and vectorizer to disk...")
    dump(model, MODEL_OUTPUT_PATH)
    dump(vectorizer, VECTORIZER_OUTPUT_PATH)
    
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    print(f"Vectorizer saved to: {VECTORIZER_OUTPUT_PATH}")
    print("--- Training Script Finished ---")


if __name__ == "__main__":
    main()