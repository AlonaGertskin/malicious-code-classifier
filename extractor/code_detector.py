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
        # detected_blocks = [] # Stores blocks of code
        code_fragments = []

                # Collect all code-like lines
        for i, line in enumerate(lines):
            scores = self.identify_language_for_line(line)
            max_score = max(scores.values()) if scores else 0
            
            if max_score >= 0.4: # threshold
                code_fragments.append({
                    'line_num': i,
                    'content': line,
                    'language': max(scores, key=scores.get),
                    'score': max_score
                })
        # i = 0
        # while i < len(lines):
        #     if self.line_contains_code_patterns(lines[i]): # Checks if the text has patterns
        #         block = self.extract_block(lines, i)
        #         if block: # If the block isnt empty
        #             detected_blocks.append(block) # Enters the block into the detected_blocks
        #             i = block['end_line'] # Goes to the end of the line
        #         else:
        #             i += 1
        #     else:
        #         i += 1
        
        return self.group_by_language(code_fragments)

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
        """
        Extract a complete code block starting from given line
        Might not use because code could be fragmented and not in blocks
        """
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
        """
        Identify the programming language of a code block
        Might not use because code could be fragmented and need to 
        identify language by line and not block
        """
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

    def identify_language_for_line(self, line):
        """Return language scores for a single line"""
        scores = {}
        
        for lang, patterns in self.patterns.items():
            if lang == 'common':
                continue
                
            score = 0
            for pattern, weight in patterns.values():
                if re.search(pattern, line):
                    score += weight
            
            scores[lang] = score
        
        return scores

    def group_by_language(self, fragments):
        """Group fragments by language, keeping sequence order"""
        groups = []
        
        # Get languages from patterns (excluding 'common')
        available_languages = [lang for lang in self.patterns.keys() if lang != 'common']
        
        for lang in available_languages:
            lang_fragments = [f for f in fragments if f['language'] == lang]
            
            if lang_fragments:
                lang_fragments.sort(key=lambda x: x['line_num'])
                groups.append(self.create_block_from_fragments(lang_fragments))
        
        return groups

    def create_block_from_fragments(self, fragments):
        """Convert list of fragments into block format"""
        return {
            'content': [f['content'] for f in fragments],
            'start_line': fragments[0]['line_num'],
            'end_line': fragments[-1]['line_num'],
            'language': fragments[0]['language'],
            'confidence': sum(f['score'] for f in fragments) / len(fragments) # placeholder
        }