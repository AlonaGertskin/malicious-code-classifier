import time
import sys
import os

# --- Color Definitions ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_slow(str_to_print, delay=0.02):
    """Prints text character by character."""
    for char in str_to_print:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_demo():
    # 1. Create dummy filename
    filename = "suspect_script.py"
    
    # Clear screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Colors.HEADER}--- Starting Hybrid Code Classifier CLI ---{Colors.ENDC}")
    time.sleep(0.5)
    print(f"User Input: Scanning file '{Colors.BOLD}{filename}{Colors.ENDC}'...")
    print("--------------------------------------------------")
    time.sleep(0.8)

    # 2. Stage 1 Simulation - Code Detection
    print(f"{Colors.CYAN}[+] Stage 1: Code Detection Engine (Heuristic){Colors.ENDC}")
    time.sleep(0.5)
    print(f"    -> Scanning for language patterns...", end=" ")
    time.sleep(0.8)
    print(f"{Colors.GREEN}[DONE]{Colors.ENDC}")
    print(f"    -> Identified Language: {Colors.BOLD}PYTHON{Colors.ENDC}")
    print(f"    -> Structural Integrity Check: {Colors.GREEN}PASSED{Colors.ENDC}")
    print(f"    -> Code Density Score: 0.85 (Threshold: 0.4)")
    print(f"    -> Action: Forwarding to AI Classifier.")
    time.sleep(0.5)
    print()

    # 3. Stage 2 Simulation - Feature Extraction & AI
    print(f"{Colors.CYAN}[+] Stage 2: AI Analysis Engine (Random Forest){Colors.ENDC}")
    time.sleep(0.5)
    print(f"    -> Loading Model (malicious_code_classifier.joblib)...", end=" ")
    time.sleep(0.8)
    print(f"{Colors.GREEN}[LOADED]{Colors.ENDC}")
    
    print(f"    -> Extracting Features (TF-IDF + N-Grams)...", end=" ")
    time.sleep(0.6)
    print(f"{Colors.GREEN}[DONE]{Colors.ENDC}")
    
    print(f"    -> Calculating Risk Score...", end=" ")
    time.sleep(1.0)
    print(f"{Colors.WARNING}[HIGH]{Colors.ENDC}")
    
    print(f"    -> Suspicious Indicators Found:")
    print(f"       * 'os.system' (Execution)")
    print(f"       * 'nc -e' (Reverse Shell Pattern)")
    time.sleep(0.5)
    print("--------------------------------------------------")
    
    # 4. Final Verdict
    time.sleep(0.5)
    print(f"{Colors.FAIL}{Colors.BOLD}[RESULT] CLASSIFICATION: MALICIOUS FILE DETECTED{Colors.ENDC}")
    print(f"Confidence Level: {Colors.WARNING}98.4%{Colors.ENDC}")
    print("Recommendation: Quarantined immediately.")
    print()

if __name__ == "__main__":
    show_demo()