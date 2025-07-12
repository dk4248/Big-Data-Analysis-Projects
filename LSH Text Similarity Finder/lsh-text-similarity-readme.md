# LSH Text Similarity Finder

## Locality Sensitive Hashing for Document Retrieval

---

## 📋 Project Overview

This project implements a Locality Sensitive Hashing (LSH) based system to find the top-5 most similar text documents for each sample in a dataset. The system mimics a ground truth similarity mapping and evaluates performance through intersection scores, providing insights through statistical analysis and visualizations.

## 🎯 Objectives

1. **Implement LSH** for efficient similarity search in high-dimensional text data
2. **Retrieve Top-5** most similar documents for each text sample
3. **Evaluate Performance** against ground truth using intersection scores
4. **Visualize Results** through histograms, box plots, and statistical summaries
5. **Support Test Data** for scalable similarity retrieval

## 📊 Dataset Description

### Input Files
- **`ids.txt`**: Contains unique identifiers for each text sample (one per line)
- **`texts.txt`**: Contains the actual text content (one sample per line)
- **`items.json`**: Ground truth mapping - each ID mapped to its 5 most similar IDs

### Test Files (for evaluation)
- **`test_ids.txt`**: IDs of test samples
- **`test_texts.txt`**: Text content of test samples

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Core Libraries**:
  - NumPy - Numerical computations
  - Pandas - Data manipulation and statistics
  - Scikit-learn - Text vectorization and utilities
  - Matplotlib/Seaborn - Visualizations
  - NLTK/SpaCy - Text preprocessing (optional)
- **LSH Implementation**: 
  - datasketch (MinHash LSH)
  - OR custom implementation

## 📁 Project Structure

```
lsh-text-similarity/
│
├── data/
│   ├── ids.txt                    # Document IDs
│   ├── texts.txt                  # Document texts
│   ├── items.json                 # Ground truth similarities
│   └── test/                      # Test data directory
│       ├── test_ids.txt
│       └── test_texts.txt
│
├── src/
│   ├── lsh_model.py              # Core LSH implementation
│   ├── text_preprocessor.py      # Text cleaning and vectorization
│   ├── similarity_finder.py      # Main similarity search logic
│   ├── evaluator.py              # Performance evaluation metrics
│   └── visualizer.py             # Plotting and statistics
│
├── models/
│   └── saved_lsh_model.pkl       # Saved LSH model
│
├── results/
│   ├── predictions.json          # Model predictions
│   ├── evaluation_report.txt     # Performance metrics
│   ├── histogram.png             # Score distribution
│   ├── boxplot.png               # Score box plot
│   └── statistics.csv            # Detailed statistics
│
├── notebooks/
│   └── analysis.ipynb            # Exploratory analysis
│
├── requirements.txt              # Python dependencies
├── config.yaml                   # Configuration parameters
├── main.py                      # Main execution script
└── README.md                    # This file
```

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd lsh-text-similarity
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data (if using)
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 💻 Implementation Details

### LSH Configuration

The implementation uses MinHash LSH with configurable parameters:

```python
# config.yaml
lsh_params:
  num_perm: 128          # Number of permutations for MinHash
  threshold: 0.5         # Jaccard similarity threshold
  num_bands: 32          # Number of bands for LSH
  rows_per_band: 4       # Rows per band (num_perm = num_bands * rows_per_band)
  
text_processing:
  min_token_length: 3    # Minimum token length
  use_stemming: true     # Apply stemming
  remove_stopwords: true # Remove stop words
  ngram_range: [1, 3]    # Use unigrams, bigrams, and trigrams
```

### Algorithm Flow

1. **Text Preprocessing**
   - Tokenization
   - Lowercasing
   - Stopword removal (optional)
   - Stemming/Lemmatization (optional)
   - N-gram generation

2. **MinHash Generation**
   - Convert text to shingles/n-grams
   - Generate MinHash signatures
   - Store in LSH index

3. **Similarity Search**
   - Query LSH index for candidates
   - Compute exact similarities for candidates
   - Return top-5 most similar items

4. **Evaluation**
   - Compare predictions with ground truth
   - Calculate intersection scores
   - Generate statistics and visualizations

## 📈 Evaluation Metrics

### Intersection Score
For each document, the intersection score is calculated as:
```
score_i = |predicted_top5_i ∩ ground_truth_top5_i|
```
Where the score ranges from 0 to 5.

### Overall Performance
```
average_score = (Σ score_i) / N
```
Where N is the total number of documents.

## 🏃 Running the Project

### 1. Train and Evaluate Model
```bash
python main.py --mode train --config config.yaml
```

### 2. Test on New Data
```bash
python main.py --mode test --test_dir data/test/ --model models/saved_lsh_model.pkl
```

### 3. Generate Visualizations Only
```bash
python src/visualizer.py --results results/evaluation_report.txt
```

### 4. Custom Parameters
```bash
python main.py --num_perm 256 --threshold 0.3 --num_bands 64
```

## 📊 Expected Output

### 1. Predictions File (`predictions.json`)
```json
{
  "doc_001": ["doc_045", "doc_123", "doc_567", "doc_890", "doc_234"],
  "doc_002": ["doc_111", "doc_222", "doc_333", "doc_444", "doc_555"],
  ...
}
```

### 2. Evaluation Report
```
LSH Text Similarity Evaluation Report
=====================================
Total Documents: 1000
Average Intersection Score: 3.42/5.00
Standard Deviation: 1.23

Score Distribution:
Score 0: 45 documents (4.5%)
Score 1: 123 documents (12.3%)
Score 2: 234 documents (23.4%)
Score 3: 298 documents (29.8%)
Score 4: 201 documents (20.1%)
Score 5: 99 documents (9.9%)
```

### 3. Visualizations
- **Histogram**: Distribution of intersection scores
- **Box Plot**: Statistical summary of scores
- **Statistics Table**: Detailed metrics (mean, std, quartiles, etc.)

## 🔧 Performance Optimization Tips

1. **Adjust LSH Parameters**
   - Increase `num_perm` for better accuracy
   - Tune `threshold` based on your similarity requirements
   - Balance `num_bands` and `rows_per_band`

2. **Text Preprocessing**
   - Experiment with different n-gram ranges
   - Try character-level shingles for short texts
   - Consider TF-IDF weighting

3. **Alternative Approaches**
   - SimHash for detecting near-duplicates
   - Random Projection LSH for dense vectors
   - Ensemble multiple LSH functions

## 📝 Assignment Deliverables

1. **Source Code**: Complete implementation with comments
2. **Predictions**: JSON file with top-5 predictions for all samples
3. **Evaluation Report**: Performance metrics and analysis
4. **Visualizations**: Histogram, box plot, and statistics
5. **Documentation**: Code documentation and usage instructions

## 🤝 References

- [MinHash Tutorial](http://infolab.stanford.edu/~ullman/mmds/ch3.pdf)
- [datasketch Documentation](https://ekzhu.github.io/datasketch/)
- [LSH Forest Paper](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/LSH-Forest.pdf)

---

