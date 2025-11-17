import re
import pandas as pd

# dictionaries mapping sensitive API calls to their risk scores
C_SENSITIVE_APIS = {
    # Code Injection / Windows API (Based on your research - High Risk)
    'VirtualAlloc': 5,          # Memory allocation for shellcode
    'VirtualProtect': 5,        # Change memory permissions (Execution)
    'CreateRemoteThread': 5,    # Remote process injection
    'RtlMoveMemory': 4,         # Used to copy payload/shellcode
    'WriteProcessMemory': 5,    # Write payload to external process
    'CryptUnprotectData': 5,    # Decrypt sensitive data (DPAPI)
    'CreateThread': 4,          # Create local thread for payload
    'WaitForSingleObject': 3,   # Control flow/delay
    
    # Standard C / Process Execution (General High Risk)
    'system(': 5,               # Execute system commands (CLI)
    'exec': 5,                  # Execute new process (execve, execl, etc.)
    
    # Networking / I/O (Medium Risk)
    'socket(': 4,
    'connect(': 4,
    'fopen(': 3,
    'fwrite(': 3,
    'SetFileAttributes': 3,     # File manipulation (e.g., hiding persistence files)
    
    # Memory Management (Lower Risk, but useful for Overflow detection)
    'malloc(': 1,
    'realloc(': 1,
    'free(': 1,
}

PYTHON_SENSITIVE_APIS = {
    # Execution and Command Injection (Python)
    'os.system': 5,
    'subprocess.Popen': 5,
    'eval(': 4,
    'exec(': 4,
    '__import__': 4,
    
    # Keylogging / Data Access (Based on your research - Python Specific)
    'pyWinhook': 5,            # Global keyboard/mouse events (Keyloggers)
    'pyperclip': 4,            # Clipboard access (Clippers)
    'win32gui': 4,             # Low-level Windows access
    'psutil': 3,               # Process information/spyware
    'sys.addaudithook': 3,     # System self-monitoring bypass
    
    # Networking and Data Exfiltration
    'socket.socket': 5,
    'requests.get': 3,
    'urllib.request.urlopen': 3,
    'Webhooks': 4,             # Discord/Slack exfiltration
    
    # Decoding and Obfuscation
    'base64.b64decode': 3,
    'marshal.loads': 4,
}

def calculate_api_risk_score(content, language):
    """
    Calculates a maliciousness risk score based on the presence of sensitive API calls.

    Args:
        content (str): The code content to analyze.
        language (str): The programming language ('python' or 'c').

    Returns:
        float: The total risk score for the content.
    """
    score = 0
    apis_to_check = {}

    if language == 'c':
        apis_to_check = C_SENSITIVE_APIS
    elif language == 'python':
        apis_to_check = PYTHON_SENSITIVE_APIS
    else:
        # Handling for unknown languages - will return 0
        return 0

    # Search logic
    if language == 'c':
        # Case-insensitive search for C APIs (common for Windows APIs and system calls)
        for api, risk in apis_to_check.items():
            # Escape the API name to handle special regex characters
            pattern_base = re.escape(api)

            # Use word boundaries for most function names, unless it ends with '('
            if api.endswith('('):
                pattern = pattern_base
            else:
                # For Windows API calls like VirtualAlloc (needs word boundaries)
                pattern = r'\b' + pattern_base + r'\b'
            
            # Find all occurrences and add to score
            matches = re.findall(pattern, content, re.IGNORECASE)
            score += len(matches) * risk

    elif language == 'python':
        # Case-sensitive search for Python APIs (typical convention)
        for api, risk in apis_to_check.items():
            # Escape API name to handle special regex characters like '.' or '('
            pattern = re.escape(api)
            
            # Find all occurrences and add to score (case sensitive for Python)
            matches = re.findall(pattern, content)
            score += len(matches) * risk

    return score

def extract_malicious_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the API risk score calculation to each entry in the DataFrame
    and adds the 'api_risk_score' feature.

    Args:
        df (pd.DataFrame): DataFrame containing 'content' and 'language' columns.

    Returns:
        pd.DataFrame: The DataFrame with the new 'api_risk_score' column.
    """
    # Use .apply(..., axis=1) to process each row, passing content and language to the calculator
    df['api_risk_score'] = df.apply(
        lambda row: calculate_api_risk_score(row['content'], row['language']),
        axis=1
    )
    return df