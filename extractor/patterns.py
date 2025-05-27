PYTHON_PATTERNS = {
    'keywords': (r'\b(def|class|import|return|if|else|while|for)\b', 0.3),
    'function_def': (r'def\s+\w+\s*\(.*\):', 0.8),
    'builtin_functions': (r'\b(print|len|range|open|input|return)\s*\(', 0.5),
    'indentation': (r'^    \w+.*$', 0.3),
    'comments': (r'#.*$', 0.2),
    'multiline_comments': (r"'''[\s\S]*?'''", 0.4),
    'string_literals': (r'["\'].*["\']', 0.2),  # Increased weight
    'docstring_start': (r'"""', 0.5), 
    'docstring_end': (r'"""', 0.5), 
    'json_structure': (r'["\'][^"\']*["\']:\s*[\[\{]', 0.6),
    'data_assignment': (r'\w+\s*=\s*[\[\{]', 0.5),  
    'multiline_call': (r'\w+\s*\(\s*$', 0.6),
    'closing_brace': (r'^\s*[}\]\)]\s*$', 0.5),
    'object_literal': (r'\{[^}]*:', 0.6),  # Added to Python
    'dict_item': (r'["\'][^"\']*["\']:\s*[^,}\]]+', 0.5),  # "key": value
    'list_with_dicts': (r'\[.*\{.*\}.*\]', 0.7),  # [{...}]
    'function_params': (r'\(\s*\w+\s*,', 0.4),  # Inside parentheses only
    'indented_param': (r'^\s{4,}\w+\s*,', 0.3),  # Indented parameters
}

C_PATTERNS = {
    'function_def': (r'\w+\s+\w+\s*\([^)]*\)\s*\{', 0.7),
    'includes': (r'#include\s*[<"][^>"]+[>"]', 0.8),
    'builtin_functions': (r'\b(printf|scanf|malloc|free|strlen|return)\s*[\(;]?', 0.4),
    'comments': (r'//.*$', 0.2),
    'multiline_comments': (r'/\*[\s\S]*?\*/', 0.4),
    'data_types': (r'\b(int|char|float|double|void)\b', 0.4),
    'preprocessor': (r'#(define|ifdef|ifndef|endif)', 0.5),
    'comment_start': (r'/\*', 0.5), 
    'comment_end': (r'\*/', 0.5), 
    'closing_brace': (r'^\s*[}\]\)]\s*$', 0.5),
    'object_literal': (r'\{[^}]*:', 0.6),
}

COMMON_PATTERNS = {
    'operators': (r'[+\-*/=<>!&|]+', 0.1),
    'brackets': (r'[(){}\[\]]', 0.2),  # Increased weight
    'semicolon': (r';', 0.2),
    'numbers': (r'\b\d+\b', 0.1),
    'function_call': (r'\w+\s*\(', 0.4),  # Reduced to avoid over-weighting
    'parameter_list': (r',\s*\w+', 0.2),  # Reduced
    'assignment': (r'\w+\s*=\s*', 0.3),  # Simplified pattern
    'array_access': (r'\w+\[.*\]', 0.4),
    'comma_separated': (r',\s*["\w]', 0.2),  # Detects lists/arrays
}