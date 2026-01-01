Malicious Code Classifier

A hybrid machine learning pipeline designed to detect and classify malicious code snippets (Python and C) within mixed text files. This project combines heuristic pattern matching with statistical feature extraction to achieve high accuracy with low false positive rates.

📌 Overview

The system operates in a two-stage pipeline:

Stage 1: Code Detector (Heuristic/Regex)

Filters out non-code text (natural language) to prevent noise.

Uses language-specific patterns (Python/C) defined in extractor/patterns.py.

Goal: High recall for code blocks.

Stage 2: Malicious Classifier (ML)

Analyzes the detected code blocks using TF-IDF vectorization.

Classifies code as Benign or Malicious using a Random Forest model.

Goal: High precision in identifying threats.

🚀 Key Features

Hybrid Approach: Combines rule-based detection with Machine Learning.

Multi-Language Support: Currently optimized for Python and C.

Noise Filtering: Effectively distinguishes between technical discussions (StackOverflow style) and executable code.

High Performance:

Overall Accuracy: ~96.5%

False Positive Rate: < 0.2% (Excellent for security tools)

📂 Project Structure

├── classifier/          # Model training and dataset building
│   ├── build_dataset.py # Script to compile CSV from raw files
│   └── ...
├── data/                # Dataset storage (Benign, Malicious, Non-code)
├── extractor/           # Stage 1: Code Detection Logic
│   ├── code_detector.py # Main detector class
│   ├── patterns.py      # Regex patterns for C and Python
│   └── __init__.py
├── tests/               # Unit and Integration tests
│   ├── full_pipeline_test.py
│   └── test_detector.py
├── detect_code.py       # CLI tool for single file detection
├── requirements.txt     # Python dependencies
└── README.md


🛠️ Installation

Clone the repository:

git clone [https://github.com/AlonaGertskin/malicious-code-classifier.git](https://github.com/AlonaGertskin/malicious-code-classifier.git)
cd malicious-code-classifier


Install dependencies:

pip install -r requirements.txt


(Note: Requires scikit-learn, pandas, numpy, matplotlib)

💻 Usage

1. Detect Code in a Single File

To scan a specific text file for code blocks:

python detect_code.py path/to/file.txt --output results.txt


2. Run the Full Pipeline Test

To validate the entire system against the dataset (Benign, Malicious, and Non-code):

python full_pipeline_test.py


3. Build/Update Dataset

If you have added new samples to the data/ directories:

python build_dataset.py


📊 Performance Results

Based on the latest validation run (pipeline_test_summary.txt):

Metric

Result

Total Files Tested

2079

Overall Accuracy

96.49%

False Positive Rate

0.19%

Detection Time

~0.11s per file

Detection Capabilities

C Files: 99.82% detection rate.

Python Files: 87.77% detection rate.

Non-Code Handling: 93.5% of pure text files were correctly filtered out at Stage 1.

📈 Visualization

The project includes scripts to visualize the pipeline and comparison results:

image.py: Generates the pipeline architecture diagram.

image2.py: Generates a comparison table against other methods.

🤝 Contributing

Contributions are welcome! Please ensure any new code patterns are added to extractor/patterns.py with appropriate weights.

📜 License

MIT License
