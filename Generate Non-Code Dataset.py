import os
import random
import shutil

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'non_code')
NUM_FILES = 1000

# Technical vocabulary (safe words)
tech_words = [
    'algorithm', 'binary', 'stack', 'overflow', 'memory', 'cpu', 'compile', 
    'execution', 'variable', 'function', 'class', 'object', 'interface', 'api', 
    'database', 'server', 'client', 'request', 'response', 'latency', 'bandwidth', 
    'encryption', 'token', 'authentication', 'deployment', 'repository', 'commit',
    'branch', 'merge', 'pull', 'push', 'clone', 'fork', 'issue', 'bug', 'feature',
    'json', 'xml', 'html', 'css', 'sql', 'nosql', 'regex', 'parsing', 'syntax',
    'recursion', 'iteration', 'pointer', 'reference', 'garbage', 'collection',
    'buffer', 'hex', 'decimal', 'loop', 'statement', 'expression', 'operator'
]

# Keywords appearing in code (used very sparsely)
code_keywords = [
    'if', 'else', 'elif', 'while', 'for', 'do', 'return', 'break', 'continue', 'switch', 
    'case', 'default', 'try', 'catch', 'finally', 'throw', 'raises', 'import', 'include', 
    'package', 'namespace', 'using', 'public', 'private', 'protected', 'static', 'void', 
    'int', 'float', 'char', 'bool', 'boolean', 'true', 'false', 'null', 'nil', 'undefined',
    'struct', 'union', 'enum', 'typedef', 'const', 'volatile', 'virtual', 'override'
]

verbs = [
    'is', 'are', 'was', 'were', 'can', 'could', 'should', 'would', 'will', 'might', 
    'must', 'processing', 'computing', 'calculating', 'generating', 'handling',
    'managing', 'optimizing', 'refactoring', 'debugging', 'testing', 'deploying',
    'compiling', 'linking', 'loading', 'executing', 'crashing', 'throwing'
]

common_words = [
    'the', 'a', 'an', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 
    'up', 'about', 'into', 'over', 'after', 'beneath', 'under', 'above', 'this',
    'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
    'some', 'any', 'all', 'no', 'every', 'each', 'check', 'verify', 'validate'
]

connectors = [
    'and', 'but', 'or', 'nor', 'for', 'yet', 'so', 'because', 'although', 'while', 
    'where', 'when', 'if', 'unless', 'until', 'since', 'before', 'after', 'then'
]

def get_tricky_element():
    """
    Generates a single token that looks like code syntax.
    """
    rand = random.random()
    word = random.choice(tech_words)
    
    if rand < 0.2:
        return f"{word}()"          # function()
    elif rand < 0.4:
        return f"{word}[i]"         # array[i]
    elif rand < 0.5:
        return f"<{word}>"          # <tag>
    elif rand < 0.6:
        return f"'{word}'"          # 'string'
    elif rand < 0.7:
        return f"Get{word.capitalize()}" # CamelCase
    elif rand < 0.8:
        return f"{word}_val"        # snake_case
    elif rand < 0.9:
        return f"{{ {word} }}"      # { block }
    else:
        return f"->{word}"          # pointer arrow

def generate_clean_sentence():
    """
    Generates a standard sentence with technical words but NO code syntax.
    """
    length = random.randint(8, 20)
    sentence = []
    for _ in range(length):
        rand_val = random.random()
        if rand_val < 0.30:
            word = random.choice(tech_words)
        elif rand_val < 0.55:
            word = random.choice(verbs)
        elif rand_val < 0.85:
            word = random.choice(common_words)
        else:
            word = random.choice(connectors)
        sentence.append(word)
    
    return " ".join(sentence).capitalize() + "."

def generate_tricky_sentence():
    """
    Generates a sentence that includes exactly ONE code-like element or keyword.
    """
    length = random.randint(10, 25)
    sentence = []
    
    # Decide randomly where to insert the code element
    insert_pos = random.randint(0, length - 1)
    
    for i in range(length):
        if i == insert_pos:
            # Insert the tricky part here
            if random.random() < 0.5:
                word = random.choice(code_keywords)
            else:
                word = get_tricky_element()
        else:
            # Standard word generation
            rand_val = random.random()
            if rand_val < 0.30:
                word = random.choice(tech_words)
            elif rand_val < 0.55:
                word = random.choice(verbs)
            elif rand_val < 0.85:
                word = random.choice(common_words)
            else:
                word = random.choice(connectors)
        
        sentence.append(word)
        
    return " ".join(sentence).capitalize() + "."

def generate_content():
    """
    Creates the file content.
    Constraints:
    - At least 10 lines long.
    - Max 1-2 occurrences of code-like elements per file.
    """
    num_lines = random.randint(10, 20)
    lines = []
    
    # Decide how many tricky lines to have in this file (1 or 2)
    num_tricky_lines = random.randint(1, 2)
    
    # Randomly choose which line numbers will be tricky
    tricky_indices = set(random.sample(range(num_lines), num_tricky_lines))
    
    for i in range(num_lines):
        if i in tricky_indices:
            lines.append(generate_tricky_sentence())
        else:
            lines.append(generate_clean_sentence())
            
    return "\n".join(lines)

def main():
    print(f"[*] Creating output directory: {OUTPUT_DIR}")
    
    if os.path.exists(OUTPUT_DIR):
        try:
            shutil.rmtree(OUTPUT_DIR)
        except OSError as e:
            print(f"[!] Error removing directory: {e}")
            return
            
    os.makedirs(OUTPUT_DIR)

    print(f"[*] Generating {NUM_FILES} text files...")
    print("    - Minimum 10 lines per file.")
    print("    - Code elements appear only 1-2 times per file.")
    
    for i in range(NUM_FILES):
        filename = f"text_sample_{i:04d}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        content = generate_content()
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            print(f"[!] Error writing file {filename}: {e}")

    print(f"[v] Successfully generated {NUM_FILES} files in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()