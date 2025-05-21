import re
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
        """
        Main method Scans text content to identify and extract potential code snippets.
    
        This method processes text line by line, looking for patterns that indicate
        programming code in supported languages (currently Python and C). When code-like
        patterns are detected, it attempts to extract complete code blocks by determining
        their boundaries and contents.
        
        Args:
            text (str): The input text to scan for code snippets

        TODO:    
        Returns:
            list: A list of dictionaries, each containing details about a detected code block:
                - 'content': List of strings (code lines)
                - 'start_line': Index of the first line of the block
                - 'end_line': Index of the last line of the block
                - 'language': Identified programming language ('python', 'c', or None)
                if time permitting:
                - 'confidence': Detection confidence score (0.0-1.0)
        """
        lines = text.split('\n')
        detected_blocks = [] #stores blocks of code
        
        i = 0
        while i < len(lines):
            if self.line_contains_code_patterns(lines[i]): #Checks if the text has patterns
                block = self.extract_block(lines, i)
                if block: #if the block isnt empty
                    detected_blocks.append(block)#enters the block into the detected_blocks
                    i = block['end_line']#goes to the end of the line
                else:
                    i += 1
            else:
                i += 1
        
        return detected_blocks

def line_contains_code_patterns(self, line):
    """
    Check if a line contains code patterns
    fast boolean check for the initial scan
    TODO
    adding a evaluate_code_patterns function that 
    does detailed analysis of code patterns with weighted scoring for patterns
    """
    # Check against all patterns
    for lang_patterns in self.patterns.values():
        for pattern in lang_patterns.values():
            if re.search(pattern, line):
                return True
    return False

def extract_block(self, lines, start_idx):
    """Extract a complete code block starting from given line"""
    block = {
        'content': [],
        'start_line': start_idx,
        'end_line': start_idx,
        'language': None,
        'confidence': 0.0
    }
    
    # Extract block based on indentation or braces
    # TODO
    # To be implemented
    
    return block if block['content'] else None

def identify_language(self, code_block):
    """Identify the programming language of a code block"""
    scores = {}
    content = '\n'.join(code_block['content'])
    
    for lang, patterns in self.patterns.items():
        if lang == 'common':  # Skip common patterns that don't indicate a specific language
            continue
            
        score = 0
        for pattern in patterns.values():
            matches = re.findall(pattern, content) # Find all matches for this pattern
            score += len(matches) # Increment score by number of matches
        
        scores[lang] = score
    
    # Determine the best match (language with highest score)
    if scores:
        best_language = max(scores.items(), key=lambda x: x[1])
        return best_language[0] if best_language[1] > 0 else None
    
    return None




