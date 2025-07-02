# Pattern format: (regex_pattern, positive_weight, {language: penalty_weight})
# positive_weight: score added when pattern matches
# penalty_weight: score subtracted from other languages when this pattern matches
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
    'python_decorators': (r'@\w+', 0.9, {'c': 0.95}),
    'yield_statement': (r'^\s*yield\s+', 0.9, {'c': 0.9}),
    'python_opening_brace': (r'^\s*\{\s*$', 0.7, {'c': 0.3}),
    'python_closing_brace': (r'^\s*\}\s*$', 0.7, {'c': 0.3}),
    'import_statement': (r'^\s*(import|from)\s+\w+', 0.9, {'c': 0.95}),
    'import_as': (r'^\s*import\s+\w+\s+as\s+\w+', 0.9, {'c': 0.95}),
    'from_import': (r'^\s*from\s+\w+\s+import', 0.9, {'c': 0.95}),
}

C_PATTERNS = {
    'includes': (r'#include\s*[<"][^>"]+[>"]', 0.9, {'python': 1.2}),
    'c_function_def': (r'\w+\s+\w+\s*\([^)]*\)\s*\{', 0.8, {'python': 1.2}),
    'data_types': (r'\b(int|char|float|double|void)\b', 0.4, {'python': 0.5}),
    'c_comments': (r'//.*$', 0.5, {'python': 0.7}),
    'multiline_comments': (r'/\*|\*/', 0.6, {'python': 0.8}),
    'preprocessor': (r'#(define|ifdef|ifndef|endif)', 0.5, {'python': 0.8}),
    'c_io': (r'\b(printf|scanf|malloc|free|strlen)\s*\(', 0.6, {'python': 0.7}),
    'return_semicolon': (r'\breturn\s.*;\s*$', 0.7, {'python': 0.6}),
    'semicolon_end': (r';\s*$', 0.3, {'python': 0.4}),
    'c_main_function': (r'int\s+main\s*\(', 1.5, {'python': 0.99}),  
    'pointer_syntax': (r'\w+\s*\*\s*\w+', 0.8, {'python': 0.9}),  
    'arrow_operator': (r'->', 0.9, {'python': 0.95}), 
    'extern_declaration': (r'extern\s+\w+', 0.6, {'python': 0.8}),
    'c_opening_brace': (r'^\s*\{\s*$', 0.8, {'python': 0.3}),
    'c_closing_brace': (r'^\s*\}\s*$', 0.8, {'python': 0.3}),
    'preprocessor_directive': (r'^\s*#\s*(define|else|endif|if|ifdef|ifndef)\b', 0.6, {'python': 0.7}),
    'spaced_define': (r'^\s*#\s+define\s+\w+', 0.7, {'python': 0.8}),
    'preprocessor_else': (r'^\s*#else\s*$', 0.6, {'python': 0.7}),
    'variable_declaration': (r'\b[a-zA-Z_]\w*_t\s+\w+.*;\s*$', 0.7, {'python': 0.8}),  # Custom types like lv_coord_t
    'multi_variable_decl': (r'\b\w+\s+\w+,\s*\w+.*;\s*$', 0.6, {'python': 0.7}),      # int x, y, z;
    'continue_statement': (r'^\s*continue\s*;\s*$', 0.8, {'python': 0.9}),   # continue;
    'break_statement': (r'^\s*break\s*;\s*$', 0.8, {'python': 0.9}),         # break;
    'c_identifier_pattern': (r'\b[a-zA-Z_]\w*_[a-zA-Z]\w*\b', 0.3, {}),  # snake_case identifiers common in C
    'multiple_vars': (r'\w+,\s*\w+', 0.4, {'python': 0.2}),              # x, y, z pattern

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
    'object_literal': (r'\{[^}]*:', 0.6, {}),
    'multiline_call': (r'\w+\s*\(\s*$', 0.6, {}),
    'data_assignment': (r'\w+\s*=\s*[\[\{]', 0.5, {}),
    'return_statement': (r'\breturn\s+\w+|return\s*$', 0.5, {}),
    'control_flow_start': (r'^\s*(if|else|while|for)\b', 0.6, {}),
    'control_flow_general': (r'\b(if|else|while|for)\b', 0.3, {}),
    'increment_ops': (r'\b\w+\+\+;?\s*$', 0.6, {}),           
    'simple_return': (r'^\s*return\s+\w+;?\s*$', 0.6, {}),
    'standalone_bracket': (r'^\s*[\]\)]\s*$', 0.7, {}),
    'bracket_combinations': (r'^\s*[\]\)\}][\]\)\}]*\s*$', 0.7, {}),
    'list_item': (r'^\s*["\']?\w+["\']?\s*,\s*$', 0.6, {}),
    'parameter_with_type': (r'^\s*\w+\s*:\s*\w+.*,\s*$', 0.7, {}),
    'line_ending_brace': (r'[}\])];\s*$', 0.6, {}),
    'simple_declaration': (r'^\s*(int|char|float|double)\s+\w+\s*;?\s*$', 0.8, {}),
    'simple_call': (r'^\s*\w+\.\w+\(\)\s*;?\s*$', 0.7, {}), 
    'simple_assignment': (r'^\s*\w+\s*=\s*\w+\s*;?\s*$', 0.6, {}),    

    # negative patterns to penalize natural language
    'articles': (r'\b(the|a|an)\s+\w+', -0.3, {}), 
    'prepositions': (r'\b(in|on|at|by|with|from|to|of)\s+\w+', -0.2, {}),
    'full_sentences': (r'\w+\s+\w+\s+\w+\s+\w+\s+\w+', -0.2, {}), 
    'past_tense': (r'\w+ed\s', -0.1, {}),
    'ordinal_numbers': (r'\b\d+(st|nd|rd|th)\b', -0.3, {}), 
    'markdown_links': (r'\[.*\]\(.*\)', -0.5, {}), 
    'citations': (r'\d+\.\s+[A-Z]', -0.4, {}),
    'question_words': (r'(?i)\b(what|how|why|when|where|which|does)\b', -0.7, {}),
    'verb_phrases': (r'\b(does|do|will|can|should)\s+\w+', -0.4, {}),
    'explanatory_phrases': (r'\b(rather than|in order to|as opposed to|let\'s|we\'re going to)\b', -0.6, {}),
    'tutorial_language': (r'\b(simply|just|now|then|next|first|finally)\s+\w+', -0.5, {}),
    'descriptive_phrases': (r'\b(this is|that is|it is|there is|this will|that will)\b', -0.6, {}),
    'measurement_talk': (r'\b(seconds|minutes|hours|records|per second|faster|slower)\b', -0.5, {}),
    'performance_discussion': (r'\b(performance|improvement|optimization|better|worse)\s+\w+', -0.5, {}),
    'result_phrases': (r'\b(imported|we can do|able to|up to)\s+\d+', -0.7, {}),
    'technical_explanations': (r'\b(by default|this guarantees|we are instructing)\b', -0.8, {}),
    'conditional_explanations': (r'\b(if|when|because|since|unless)\s+\w+\s+\w+', -0.4, {}),
    'sentence_ending': (r'\w+\s+(is|are|was|were|has|have|been)\s+\w+', -0.4, {}), 
    'conversational': (r'\b(i|you|we)\s+(can|should|need|want|have|get)\b', -0.4, {}), 
    'explanatory_verbs': (r'\b(tried|expect|tested|flagged)\s+', -0.3, {}), 
    'copyright_generic': (r'copyright|license|author', -0.6, {}), 
    'file_references': (r'\.(txt|py|c|cpp|h|js|yaml)(\s|$)', -0.4, {}),
}