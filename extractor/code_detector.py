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
        
        code_blocks =  self.group_by_language(code_fragments)
        for block in code_blocks:
            structure_info = self.analyze_structure(block['content'], block['language'], block['start_line'])
        return code_blocks
        
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
        """
        Group fragments by language, keeping sequence order
        Returns :
            list: List of dictionaries, each representing a language-specific code block:
                - 'content': List of code lines (strings)
                - 'start_line': First line number of the block (int)
                - 'end_line': Last line number of the block (int)  
                - 'language': Programming language identifier ('python', 'c', etc.)
                - 'confidence': Average confidence score for the block (float 0.0-1.0)
        """
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
    
    def count_braces_in_line(self, line, line_index ,brace_errors, counters):
        line_counts = [line.count('(') - line.count(')'),
                    line.count('[') - line.count(']'), 
                    line.count('{') - line.count('}')]
        
        for i, (brace_type, count) in enumerate(zip(['round', 'square', 'curly'], line_counts)):
            counters[i] += count
            if counters[i] > 0 and count > 0:  # New opens
                brace_errors[brace_type].extend([line_index] * count)
            elif counters[i] >= 0 and count < 0:  # Closes match opens
                for _ in range(abs(count)):
                    if brace_errors[brace_type]:
                        brace_errors[brace_type].pop()
        return 

    def handle_comment_delimiters(self, line, line_num, start_delim, end_delim, in_comment, comment_start, multiline_comments):
        if start_delim in line and not in_comment:
            comment_start = line_num
            in_comment = True
        if end_delim in line and in_comment:
            multiline_comments.append({'start': comment_start, 'end': line_num})
            in_comment = False
        
        return in_comment, comment_start

    def process_multiline_comments(self, line, line_num, language, in_comment,\
                                    comment_start, multiline_comments):
        if language == 'c':
            in_comment, comment_start = self.handle_comment_delimiters( \
                line, line_num, '/*', '*/', in_comment, comment_start, multiline_comments)
        elif language == 'python':
            in_comment, comment_start = self.handle_comment_delimiters( \
                line, line_num, '"""', '"""', in_comment, comment_start, multiline_comments)  
        return in_comment, comment_start

    def analyze_structure(self, content , language, start_line):
        multiline_comments = []
        brace_errors = {'round': [], 'square': [], 'curly': []}
        counters = [0, 0, 0]
        in_comment = False
        comment_start = None
        for i, line in enumerate(content):
            counters = self.count_braces_in_line(line, start_line + i, brace_errors, counters)
            in_comment, comment_start = self.process_multiline_comments( \
            line, start_line + i, language, in_comment, comment_start, multiline_comments)
        
        """
        TODO:
        Use the brace_errors and multiline_comments to check if all lines were correctly appended to
        the code blocks.
        """
        return {
        'multiline_comments': multiline_comments,
        'brace_errors': brace_errors
        }
            





"""
A problem the arised from the C code blocks: ending } are not being recignized as code
Another issue could be comments like """ """ in python or /* */ in C
as a solution we might use two passes to fix the structure of the code:

Pass 1 Functions:

scan_for_code_patterns(lines) - returns list of line indices with code patterns
identify_structural_elements(lines) - finds language-specific delimiters (braces, quotes, backslashes)
calculate_line_scores(lines) - scores each line for code likelihood
analyze_structure(lines) - finds language-specific delimiters (braces, quotes, backslashes) and 
identifies opening patterns (function defs, docstrings, comments)



Pass 2 Functions:

complete_multiline_constructs(boundaries, lines, language) - extends to find closing elements
extract_final_blocks(lines, refined_boundaries) - creates final code block objects

Language-specific completion:

C: match braces {} and /* */
Python: match quotes and continuation lines \

Main flow: Pass 1 → Pass 2 (language-aware) → return blocks.
"""