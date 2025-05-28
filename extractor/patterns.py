# All patterns now use format: (regex, positive_weight, {penalty_dict})
PYTHON_PATTERNS = {
    'function_def': (r'def\s+\w+\s*\(.*\):', 0.8, {'c': 0.9}),
    'python_keywords': (r'\b(class|import|elif|pass|with|as)\b', 0.4, {'c': 0.6}),
    'python_booleans': (r'\b(True|False|None)\b', 0.6, {'c': 0.7}),
    'python_self': (r'\bself\b', 0.5, {'c': 0.8}),
    'list_comprehension': (r'\[.*for\s+\w+\s+in\s+.*\]', 0.7, {'c': 0.8}),
    'docstring': (r'"""', 0.5, {'c': 0.7}),
    'python_comments': (r'#(?!include|define|ifdef|ifndef|endif).*$', 0.2, {'c': 0.4}),
    'indentation': (r'^    \w+.*$', 0.3, {'c': 0.2}),
    'python_builtins': (r'\b(print|len|range|input)\s*\(', 0.5, {'c': 0.3}),
    'json_structure': (r'["\'][^"\']*["\']:\s*[\[\{]', 0.6, {'c': 0.5}),
    'dict_item': (r'["\'][^"\']*["\']:\s*[^,}\]]+', 0.5, {'c': 0.4}),
    'list_with_dicts': (r'\[.*\{.*\}.*\]', 0.7, {'c': 0.6}),
}

C_PATTERNS = {
    'includes': (r'#include\s*[<"][^>"]+[>"]', 0.8, {'python': 0.9}),
    'c_function_def': (r'\w+\s+\w+\s*\([^)]*\)\s*\{', 0.7, {'python': 0.9}),
    'data_types': (r'\b(int|char|float|double|void)\b', 0.4, {'python': 0.5}),
    'c_comments': (r'//.*$', 0.2, {'python': 0.7}),
    'multiline_comments': (r'/\*|\*/', 0.4, {'python': 0.6}),
    'preprocessor': (r'#(define|ifdef|ifndef|endif)', 0.5, {'python': 0.8}),
    'c_io': (r'\b(printf|scanf|malloc|free|strlen)\s*\(', 0.6, {'python': 0.7}),
    'return_semicolon': (r'\breturn\s.*;\s*$', 0.5, {'python': 0.6}),
    'semicolon_end': (r';\s*$', 0.3, {'python': 0.4}),
}

COMMON_PATTERNS = {
    'brackets': (r'[(){}\[\]]', 0.2, {}),
    'function_call': (r'\w+\s*\(', 0.4, {}),
    'assignment': (r'\w+\s*=\s*', 0.3, {}),
    'array_access': (r'\w+\[.*\]', 0.4, {}),
    'operators': (r'[+\-*/=<>!&|]+', 0.1, {}),
    'numbers': (r'\b\d+\b', 0.1, {}),
    'comma_separated': (r',\s*["\w]', 0.2, {}),
    'string_literals': (r'["\'].*["\']', 0.2, {}),
    'return_keyword': (r'\breturn\b', 0.2, {}),
    'control_flow': (r'\b(if|else|while|for)\b', 0.2, {}),
    'closing_brace': (r'^\s*[}\]\)]\s*$', 0.5, {}),
    'object_literal': (r'\{[^}]*:', 0.6, {}),
    'multiline_call': (r'\w+\s*\(\s*$', 0.6, {}),
    'data_assignment': (r'\w+\s*=\s*[\[\{]', 0.5, {}),
}