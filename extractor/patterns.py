PYTHON_PATTERNS = {
   # Matches common Python keywords
   'keywords': r'\b(def|class|import|return|if|else|while|for)\b',
   # Matches function definition syntax: def function_name():
   'function_def': r'def\s+\w+\s*\(.*\):',
   # Matches Python's 4-space indentation at the start of a line
   'indentation': r'^    \w+.*$',
   # Matches single-line comments starting with #
   'comments': r'#.*$',
   # Matches strings in single or double quotes
   'string_literals': r'["\'].*["\']'
}

C_PATTERNS = {
   # Matches C function definitions: type name(params) {
   'function_def': r'\w+\s+\w+\s*\([^)]*\)\s*\{',
   # Matches #include directives with angle or quote brackets
   'includes': r'#include\s*[<"][^>"]+[>"]',
   # Matches single-line comments starting with //
   'comments': r'//.*$',
   # Matches multi-line comments /* ... */
   'multiline_comments': r'/\*[\s\S]*?\*/',
   # Matches C data types
   'data_types': r'\b(int|char|float|double|void)\b'
    # Matches C preprocessor directives
   'preprocessor': r'#(define|ifdef|ifndef|endif)'
   }
