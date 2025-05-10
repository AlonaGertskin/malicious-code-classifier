from .patterns import PYTHON_PATTERNS, C_PATTERNS, COMMON_PATTERNS

class CodeDetector:
    def __init__(self):
        """
        Initialize the code detector with patterns for different languages.
        """
        self.patterns = {
            'python': PYTHON_PATTERNS,    # Python-specific patterns
            'c': C_PATTERNS,              # C-specific patterns
            'common': COMMON_PATTERNS     # Patterns shared across languages
        }

   def detect_code(self, text):
    lines = text.split('\n')
    detected_blocks = []#stores blocks of code
    
    i = 0
    while i < len(lines):
        if self._is_code_like(lines[i]):#Checks if the text has patterns
            block = self._extract_block(lines, i)
            if block:#if the block isnt empty
                detected_blocks.append(block)#enters the block into the detected_blocks
                i = block['end_line']#goes to the end of the line
            else:
                i += 1
        else:
            i += 1
    
    return detected_blocks

def _is_code_like(self, line):
    """Check if a line contains code patterns"""
    # Check against all patterns
    for lang_patterns in self.patterns.values():
        for pattern in lang_patterns.values():
            if re.search(pattern, line):
                return True
    return False

def _extract_block(self, lines, start_idx):
    """Extract a complete code block starting from given line"""
    block = {
        'content': [],
        'start_line': start_idx,
        'end_line': start_idx,
        'language': None,
        'confidence': 0.0
    }
    
    # Extract block based on indentation or braces
    # To be implemented
    
    return block if block['content'] else None

def _identify_language(self, code_block):
    """Identify the programming language of a code block"""
    scores = {}
    content = '\n'.join(code_block['content'])
    
    for lang, patterns in self.patterns.items():
        if lang == 'common':
            continue
            
        score = 0
        for pattern in patterns.values():
            matches = re.findall(pattern, content) #finds matches in patterns
            score += len(matches)
        
        scores[lang] = score
    
    # Return language with highest score
    if scores:
        best_language = max(scores.items(), key=lambda x: x[1])
        return best_language[0] if best_language[1] > 0 else None
    
    return None




