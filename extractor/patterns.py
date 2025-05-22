PYTHON_PATTERNS = {
    # Matches common Python keywords
    'keywords': (r'\b(def|class|import|return|if|else|while|for)\b', 0.3),
    # Matches function definition syntax: def function_name():
    'function_def': (r'def\s+\w+\s*\(.*\):', 0.8),
    'builtin_functions': (r'\b(print|len|range|open|input|return)\s*\(', 0.5),
    # Matches Python's 4-space indentation at the start of a line
    'indentation': (r'^    \w+.*$', 0.3),
    # Matches single-line comments starting with #
    'comments': (r'#.*$', 0.2),
    # Matches strings in single or double quotes
    'string_literals': (r'["\'].*["\']', 0.1)
}

C_PATTERNS = {
    # Matches C function definitions: type name(params) {
    'function_def': (r'\w+\s+\w+\s*\([^)]*\)\s*\{', 0.7),
    # Matches #include directives with angle or quote brackets
    'includes': (r'#include\s*[<"][^>"]+[>"]', 0.8),
    'builtin_functions': (r'\b(printf|scanf|malloc|free|strlen|return)\s*[\(;]?', 0.4),
    # Matches single-line comments starting with //
    'comments': (r'//.*$', 0.2),
    # Matches multi-line comments /* ... */
    'multiline_comments': (r'/\*[\s\S]*?\*/', 0.3),
    # Matches C data types
    'data_types': (r'\b(int|char|float|double|void)\b', 0.4),
    # Matches C preprocessor directives
    'preprocessor': (r'#(define|ifdef|ifndef|endif)', 0.5)
}

# Common patterns for both languages
COMMON_PATTERNS = {
    'operators': (r'[+\-*/=<>!&|]+', 0.1),
    'brackets': (r'[(){}\[\]]', 0.1),
    'semicolon': (r';', 0.2),
    'numbers': (r'\b\d+\b', 0.1)
}