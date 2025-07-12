# AGM Community Detection

## Affiliation Graph Model for GitHub Social Network Analysis using Apache Spark GraphX

---

## 📋 Project Overview

This project implements the Affiliation Graph Model (AGM) to detect communities in the GitHub social network dataset using Apache Spark GraphX. The implementation identifies overlapping communities and evaluates their quality using modularity as the primary metric.

## 🎯 Objectives

1. **Load and Process** GitHub social network data into Spark GraphX
2. **Implement AGM** for overlapping community detection
3. **Evaluate Communities** using modularity score
4. **Visualize Results** showing community structure and statistics
5. **Analyze Performance** of the AGM implementation

## 📊 Dataset

**GitHub Social Network** (from SNAP)
- **URL**: https://snap.stanford.edu/data/github-social.html
- **Nodes**: 37,700 (GitHub developers)
- **Edges**: 289,003 (mutual follower relationships)
- **Format**: Edge list (undirected graph)

Dataset characteristics:
- Developers who have at least 10 starred repositories
- Edges represent mutual follow relationships
- Large connected component with natural community structure

## 🛠️ Technology Stack

- **Apache Spark 3.x** with GraphX
- **Python** (PySpark) or **Scala**
- **Libraries**:
  - PySpark
  - NetworkX (for visualization only)
  - Matplotlib/Seaborn
  - NumPy, Pandas

## 📁 Project Structure

```
agm-community-detection/
│
├── data/
│   ├── musae_git_edges.csv      # GitHub social network edges
│   └── processed/               # Preprocessed graph data
│
├── src/
│   ├── agm_implementation.py    # Core AGM algorithm
│   ├── graph_loader.py          # Load data into GraphX
│   ├── modularity.py            # Modularity calculation
│   ├── community_analyzer.py    # Community analysis tools
│   └── config.py                # Configuration settings
│
├── spark_jobs/
│   ├── agm_job.py              # Main Spark job
│   └── submit_job.sh           # Job submission script
│
├── results/
│   ├── communities/            # Detected communities
│   │   ├── community_assignments.csv
│   │   └── community_stats.json
│   ├── metrics/               # Evaluation metrics
│   │   └── modularity_scores.csv
│   └── visualizations/        # Graphs and plots
│       ├── community_sizes.png
│       ├── modularity_evolution.png
│       └── network_visualization.png
│
├── notebooks/
│   ├── data_exploration.ipynb  # Initial data analysis
│   └── results_analysis.ipynb  # Result visualization
│
├── requirements.txt            # Python dependencies
├── build.sbt                  # Scala build file (if using Scala)
└── README.md                  # This file
```

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd agm-community-detection
```

### 2. Download Dataset
```bash
# Download GitHub social network data
wget https://snap.stanford.edu/data/musae_git_edges.csv -P data/
```

### 3. Setup Environment

#### For Python (PySpark):
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### For Scala:
```bash
# Ensure Scala and SBT are installed
sbt compile
```

### 4. Install Spark
```bash
# Download and extract Spark
wget https://apache.org/dist/spark/spark-3.x.x/spark-3.x.x-bin-hadoop3.2.tgz
tar -xzf spark-3.x.x-bin-hadoop3.2.tgz

# Set environment variables
export SPARK_HOME=/path/to/spark
export PATH=$SPARK_HOME/bin:$PATH
```

## 💻 Implementation Details

### Affiliation Graph Model (AGM)

AGM detects overlapping communities by:

1. **Community Affiliation Matrix**: B[i,c] = strength of node i's membership in community c
2. **Edge Probability**: P(edge between i,j) = 1 - ∏(1 - p_c) for all communities c where both i,j belong
3. **Optimization**: Maximize likelihood of observed edges

Key parameters:
```python
# config.py
AGM_PARAMS = {
    'num_communities': 50,      # Initial number of communities
    'max_iterations': 100,      # Maximum iterations
    'epsilon': 1e-4,           # Convergence threshold
    'alpha': 0.1,              # Learning rate
    'min_community_size': 3    # Minimum community size
}
```

### Modularity Calculation

Modularity Q is calculated as:
```
Q = (1/2m) * Σ[A_ij - (k_i*k_j)/(2m)] * δ(c_i, c_j)
```

Where:
- A_ij = adjacency matrix
- k_i = degree of node i
- m = total number of edges
- δ(c_i, c_j) = 1 if nodes i,j in same community, 0 otherwise

## 📈 Running the Project

### 1. Data Preprocessing
```bash
# Load and preprocess the graph
python src/graph_loader.py --input data/musae_git_edges.csv
```

### 2. Run AGM Community Detection
```bash
# Submit Spark job
spark-submit \
  --master local[*] \
  --driver-memory 4g \
  --executor-memory 4g \
  spark_jobs/agm_job.py \
  --input data/processed/graph.parquet \
  --output results/communities/
```

### 3. Calculate Modularity
```bash
# Evaluate detected communities
python src/modularity.py \
  --graph data/processed/graph.parquet \
  --communities results/communities/community_assignments.csv
```

### 4. Analyze Results
```bash
# Generate analysis report
python src/community_analyzer.py --results results/
```

## 📊 Expected Output

### 1. Community Assignments
```csv
node_id,community_ids,membership_strengths
1234,"[1,5,12]","[0.8,0.6,0.3]"
5678,"[2,5]","[0.9,0.4]"
...
```

### 2. Modularity Report
```json
{
  "final_modularity": 0.425,
  "num_communities": 47,
  "avg_community_size": 156.3,
  "coverage": 0.982,
  "overlap_coefficient": 1.23
}
```

### 3. Community Statistics
- Size distribution
- Overlap analysis
- Core nodes per community
- Inter-community edges

## 🔧 Performance Optimization

### 1. Spark Configuration
```python
spark_conf = SparkConf() \
    .set("spark.graphx.pregel.checkpointInterval", "5") \
    .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .set("spark.sql.adaptive.enabled", "true") \
    .set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### 2. GraphX Optimizations
- Use vertex and edge partitioning strategies
- Cache frequently accessed RDDs
- Optimize Pregel operations

### 3. AGM Optimizations
- Use sparse matrix representations
- Implement early stopping
- Parallel community updates

## 📈 Evaluation Metrics

### Primary Metric: Modularity
- Target: Q > 0.3 (indicates good community structure)
- Compare with baseline algorithms (e.g., Label Propagation)

### Additional Metrics
1. **Community Quality**
   - Conductance
   - Internal density
   - Cut ratio

2. **Overlap Metrics**
   - Average memberships per node
   - Community overlap coefficient

3. **Computational Performance**
   - Runtime vs. graph size
   - Memory usage
   - Scalability analysis

## 📝 Analysis Tasks

1. **Community Structure Analysis**
   - Identify major communities
   - Analyze community themes (if metadata available)
   - Study overlap patterns

2. **Modularity Analysis**
   - Compare AGM modularity with other algorithms
   - Study modularity vs. number of communities
   - Analyze convergence behavior

3. **Scalability Study**
   - Performance on graph samples of different sizes
   - Spark resource utilization
   - Optimization impact

## 🤝 Deliverables

1. **Implementation**
   - Complete AGM implementation in Spark GraphX
   - Modularity calculation code
   - Analysis scripts

2. **Results**
   - Detected communities with membership strengths
   - Modularity scores and evolution
   - Community statistics

3. **Report**
   - Algorithm implementation details
   - Experimental results
   - Comparison with baseline methods
   - Performance analysis

4. **Visualizations**
   - Community size distribution
   - Modularity convergence plot
   - Sample community visualizations

## 🐛 Troubleshooting

### Common Issues

1. **Out of Memory Error**
```bash
# Increase executor memory
spark-submit --executor-memory 8g --driver-memory 8g agm_job.py
```

2. **Slow Convergence**
- Adjust learning rate (alpha)
- Implement adaptive learning rate
- Check for disconnected components

3. **Poor Modularity**
- Try different initial community numbers
- Check graph preprocessing
- Verify AGM implementation

## 📚 References

- [AGM Paper - Yang & Leskovec](http://www.cs.cornell.edu/home/kleinber/icml12-agm.pdf)
- [GraphX Programming Guide](https://spark.apache.org/docs/latest/graphx-programming-guide.html)
- [Modularity - Newman](https://www.pnas.org/doi/10.1073/pnas.0601602103)
- [SNAP GitHub Dataset](https://snap.stanford.edu/data/github-social.html)

