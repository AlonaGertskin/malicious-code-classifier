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