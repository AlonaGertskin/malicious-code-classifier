import os
from extractor.code_detector import CodeDetector
import glob
from datetime import datetime

# run with python -m pytest tests/test_detector.py -v -s

def save_results_to_file(results, output_file="detection_results.txt"):
    """Save detection results to a text file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Code Detection Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for result in results:
            f.write(f"File: {result['file']}\n")
            f.write(f"Total blocks: {result['total_blocks']}\n")
            f.write("-" * 40 + "\n")
            
            for block in result['blocks']:
                f.write(f"Block {block['block_number']}:\n")
                f.write(f"  Language: {block['language']}\n")
                f.write(f"  Lines: {block['start_line']}-{block['end_line']}\n")
                f.write(f"  Confidence: {block['confidence']}\n")
                f.write(f"  Content:\n")
                for line in block['content']:
                    f.write(f"    {line}\n")
                f.write("\n")
            f.write("\n")
    
    print(f"Results saved to {output_file}")

def run_file_test(filename):
    """
    Test code detection on a file.
    
    Args:
        filename (str): Path to the test file
    """
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return
    
    # Read file content
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Run detection
    detector = CodeDetector()
    result = detector.detect_code(text)
    
    # Basic assertions (modify as needed)
    assert len(result) >= 1, f"Expected at least 1 code block, found {len(result)}"
    
    # Print results
    print(f"File: {filename}")
    print(f"Detected {len(result)} code block(s):")
    
    for i, block in enumerate(result):
        print(f"\nBlock {i+1}:")
        print(f"  Language: {block.get('language', 'Unknown')}")
        print(f"  Lines: {block.get('start_line', 'N/A')} - {block.get('end_line', 'N/A')}")
        print(f"  Confidence: {block.get('confidence', 'N/A')}")
        if block.get('content'):
            print(f"  Content preview: {block['content'][:7]}...")

    # Format results for saving
    file_result = {
        "file": filename,
        "total_blocks": len(result),
        "blocks": []
    }
    
    for i, block in enumerate(result):
        block_info = {
            "block_number": i + 1,
            "language": block.get('language', 'Unknown'),
            "start_line": block.get('start_line', 'N/A'),
            "end_line": block.get('end_line', 'N/A'),
            "confidence": block.get('confidence', 'N/A'),
            "content": block.get('content', [])
        }
        file_result["blocks"].append(block_info)

    return result, file_result

def test_all_sample_files():
    """Test all files in the test samples directory"""
    test_dir = "tests/test_samples/"
    test_files = glob.glob(os.path.join(test_dir, "*.txt"))
    
    assert test_files, f"No .txt files found in {test_dir}"
    
    all_results = []
    for file_path in test_files:
        result, file_result = run_file_test(file_path)
        all_results.append(file_result)
        assert len(result) >= 0, f"Detection failed for {file_path}"
    
    save_results_to_file(all_results)

