# Citation SimRank Analysis

## Graph-based Paper Similarity using Neo4j and Apache Spark

---

## 📋 Project Overview

This project implements SimRank algorithm on a citation graph to find similar academic papers. The system builds a directed graph in Neo4j where nodes represent papers and edges represent citation relationships, then uses Apache Spark to compute SimRank similarity scores with different decay factors.

## 🎯 Objectives

1. **Graph Construction**: Build citation network in Neo4j from provided dataset
2. **SimRank Implementation**: Run SimRank algorithm using Apache Spark
3. **Parameter Analysis**: Compare results with C values {0.7, 0.8, 0.9}
4. **Similarity Search**: Find most similar papers for query nodes {2982615777, 1556418098}
5. **Performance Evaluation**: Analyze impact of decay factor on similarity scores

## 📊 Dataset Structure

The input data contains:
- **paper**: ID of the citing paper (source node)
- **reference**: List of IDs of cited papers (target nodes)

Example:
```json
{
  "paper": 123456,
  "reference": [789012, 345678, 901234]
}
```

This creates directed edges: 123456 → 789012, 123456 → 345678, 123456 → 901234

## 🛠️ Technology Stack

- **Graph Database**: Neo4j 4.x
- **Processing Framework**: Apache Spark 3.x
- **Programming Language**: Python/Scala
- **Libraries**:
  - py2neo (Neo4j Python driver)
  - PySpark
  - GraphFrames (Spark graph processing)
  - Pandas, NumPy
  - Matplotlib/Seaborn (visualization)

## 📁 Project Structure

```
citation-simrank-analysis/
│
├── data/
│   ├── citations.json            # Input citation data
│   └── processed/               # Preprocessed data files
│
├── src/
│   ├── graph_builder.py         # Neo4j graph construction
│   ├── simrank_spark.py         # SimRank implementation in Spark
│   ├── query_processor.py       # Similarity query handler
│   ├── utils.py                 # Helper functions
│   └── config.py                # Configuration settings
│
├── spark/
│   ├── simrank_job.py          # Spark job for SimRank
│   └── graph_loader.py         # Load Neo4j data into Spark
│
├── results/
│   ├── simrank_c0.7/           # Results for C=0.7
│   ├── simrank_c0.8/           # Results for C=0.8
│   ├── simrank_c0.9/           # Results for C=0.9
│   └── analysis_report.pdf     # Comparative analysis
│
├── notebooks/
│   ├── data_exploration.ipynb  # Data analysis
│   └── results_visualization.ipynb # Result visualization
│
├── scripts/
│   ├── setup_neo4j.sh          # Neo4j setup script
│   └── run_experiments.sh      # Run all experiments
│
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Neo4j Docker setup
└── README.md                  # This file
```

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd citation-simrank-analysis
```

### 2. Setup Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Neo4j

#### Option A: Using Docker
```bash
docker-compose up -d
```

#### Option B: Local Installation
```bash
# Download and install Neo4j from https://neo4j.com/download/
# Start Neo4j service
neo4j start
```

### 4. Configure Neo4j Connection
```python
# config.py
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
```

### 5. Setup Spark
```bash
# Download Spark
wget https://apache.org/dist/spark/spark-3.x.x/spark-3.x.x-bin-hadoop3.2.tgz
tar -xzf spark-3.x.x-bin-hadoop3.2.tgz

# Set environment variables
export SPARK_HOME=/path/to/spark
export PATH=$SPARK_HOME/bin:$PATH
```

## 💻 Implementation Details

### 1. Graph Construction in Neo4j

```cypher
// Create nodes
CREATE (p:Paper {id: $paper_id})

// Create citation relationships
MATCH (citing:Paper {id: $citing_id})
MATCH (cited:Paper {id: $cited_id})
CREATE (citing)-[:CITES]->(cited)
```

### 2. SimRank Algorithm

SimRank formula:
```
S(a,b) = C * (Σ S(Ii(a), Ij(b))) / (|I(a)| * |I(b)|)
```

Where:
- S(a,b) = similarity between nodes a and b
- C = decay factor (0.7, 0.8, 0.9)
- I(a) = in-neighbors of node a
- |I(a)| = number of in-neighbors

### 3. Configuration Parameters

```yaml
# config.yaml
simrank:
  max_iterations: 10
  convergence_threshold: 0.0001
  decay_factors: [0.7, 0.8, 0.9]
  
query:
  node_ids: [2982615777, 1556418098]
  top_k: 10  # Return top 10 similar papers
  
spark:
  master: "local[*]"
  app_name: "CitationSimRank"
  memory: "4g"
```

## 📈 Running the Analysis

### 1. Build Citation Graph
```bash
python src/graph_builder.py --input data/citations.json
```

### 2. Run SimRank for All C Values
```bash
# Run all experiments
bash scripts/run_experiments.sh

# Or run individually
spark-submit spark/simrank_job.py --c 0.7 --query 2982615777
spark-submit spark/simrank_job.py --c 0.8 --query 2982615777
spark-submit spark/simrank_job.py --c 0.9 --query 2982615777
```

### 3. Query Similar Papers
```bash
python src/query_processor.py --node 2982615777 --c 0.8 --top-k 10
```

## 📊 Expected Output

### 1. Similarity Results Format
```json
{
  "query_node": 2982615777,
  "decay_factor": 0.8,
  "similar_papers": [
    {"paper_id": 1234567890, "similarity": 0.875},
    {"paper_id": 9876543210, "similarity": 0.823},
    {"paper_id": 5555555555, "similarity": 0.756},
    ...
  ]
}
```

### 2. Comparative Analysis Table

| Query Node | C Value | Top-1 Similar | Score | Top-5 Avg Score |
|------------|---------|---------------|-------|-----------------|
| 2982615777 | 0.7     | 1234567890   | 0.823 | 0.756          |
| 2982615777 | 0.8     | 1234567890   | 0.875 | 0.812          |
| 2982615777 | 0.9     | 1234567890   | 0.912 | 0.865          |

### 3. Visualizations
- Similarity score distribution for each C value
- Convergence plots showing iterations vs. change in scores
- Network visualization of query nodes and their similar papers

## 🔧 Performance Optimization

### 1. Neo4j Optimizations
```cypher
// Create indexes for faster lookups
CREATE INDEX paper_id_index FOR (p:Paper) ON (p.id)

// Optimize for in-degree queries
CALL db.index.fulltext.createNodeIndex("papers", ["Paper"], ["id"])
```

### 2. Spark Optimizations
- Use GraphFrames for efficient graph operations
- Cache intermediate results
- Partition data based on node degrees
- Use broadcast variables for small lookup tables

### 3. Algorithm Optimizations
- Early termination when convergence reached
- Prune low-similarity pairs
- Use sparse matrix representations

## 📝 Analysis Tasks

1. **Impact of C Value**
   - How does the decay factor affect similarity scores?
   - Which C value produces most intuitive results?

2. **Convergence Analysis**
   - How many iterations needed for convergence?
   - Does convergence rate depend on C?

3. **Graph Statistics**
   - Node degree distribution
   - Citation patterns
   - Connected components

## 🤝 Deliverables

1. **Code Implementation**
   - Complete source code with documentation
   - Spark jobs for SimRank computation

2. **Results**
   - Similarity results for both query nodes
   - Results for all three C values
   - Comparative analysis

3. **Report**
   - Algorithm implementation details
   - Performance analysis
   - Insights from different C values

4. **Visualizations**
   - Graph structure visualization
   - Similarity score distributions
   - Convergence plots

## 📋 Troubleshooting

### Common Issues

1. **Neo4j Connection Error**
   ```bash
   # Check if Neo4j is running
   neo4j status
   # Verify credentials in config
   ```

2. **Spark Memory Issues**
   ```bash
   # Increase driver memory
   spark-submit --driver-memory 8g spark/simrank_job.py
   ```

3. **Slow Performance**
   - Ensure indexes are created in Neo4j
   - Check Spark partition count
   - Monitor memory usage

## 📚 References

- [SimRank Paper](https://www-cs.stanford.edu/~glenj/simrank.pdf)
- [NetworkX SimRank Documentation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.similarity.simrank_similarity.html)
- [Neo4j Graph Algorithms](https://neo4j.com/docs/graph-data-science/current/)
- [GraphFrames Documentation](http://graphframes.github.io/graphframes/docs/_site/)

---

