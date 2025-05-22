import pytest
from extractor.code_detector import CodeDetector

def test_detect_python_function():
    text = """
    def hello_world():
        print("Hello")
    """
    detector = CodeDetector()
    result = detector.detect_code(text)
    assert len(result) == 1
    assert result[0]['language'] == 'python'
    print(result)

def test_detect_c_function():
    text = """
    int main() {
        printf("Hello");
        return 0;
    }
    """
    detector = CodeDetector()
    result = detector.detect_code(text)
    assert len(result) == 1
    assert result[0]['language'] == 'c'
    print(result)


    '''
    Run with " python -m pytest tests/test_detector.py -v -s" in the terminal
    -s shows prints
    '''