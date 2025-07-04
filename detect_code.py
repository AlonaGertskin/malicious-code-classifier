"""
Simple Command Line Interface for Code Detection
Usage: python detect_code.py <input_file> [output_file]

Detects Python and C code snippets in text files using pattern-based analysis
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path
from extractor.code_detector import CodeDetector

def main():
    parser = argparse.ArgumentParser(
        description="Detect code snippets in text files",
        epilog="Example: python detect_code.py document.txt results.txt"
    )
    
    parser.add_argument(
        "input_file", 
        help="Path to the input text file to analyze"
    )
    
    parser.add_argument(
        "output_file", 
        nargs='?', 
        help="Path to output file (optional, defaults to input_detected.txt)"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug output showing pattern matching details"
    )
    
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.4, 
        help="Detection threshold (default: 0.4)"
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)

    # Generate output filename if not provided
    if args.output_file is None:
        input_path = Path(args.input_file)
        args.output_file = input_path.stem + "_detected.txt"

    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ Loaded file: {args.input_file} ({len(content)} characters)")
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Run detection
    print("🔍 Analyzing text for code patterns...")
    detector = CodeDetector(debug=args.debug, threshold=args.threshold)
    detected_blocks = detector.detect_code(content)
    
    # Generate report
    print(f"✓ Detection complete: Found code")
    
    # Save results as single code block
    save_code_to_file(detected_blocks, args.output_file)
    
    print(f"✅ Code saved to: {args.output_file}")


def save_code_to_file(blocks, output_file):
    """Save the detected code content to file"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        if not blocks:
            f.write("# No code detected\n")
            return
        
        # Combine all detected code blocks into one
        all_code_lines = []
        
        for block in blocks:
            if block.get('content'):
                # Add all lines from this block
                all_code_lines.extend(block['content'])
                
                # Add a blank line between blocks (optional)
                all_code_lines.append("")
        
        # Remove trailing empty lines
        while all_code_lines and all_code_lines[-1] == "":
            all_code_lines.pop()
        
        # Write all code to file
        for line in all_code_lines:
            f.write(f"{line}\n")


if __name__ == "__main__":
    main()