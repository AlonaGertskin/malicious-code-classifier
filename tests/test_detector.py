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