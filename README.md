# Big Data Analytics Projects Portfolio

## Course Assignment Collection

---

## 📚 Overview

This repository contains four comprehensive Big Data Analytics projects that demonstrate various aspects of modern data engineering, including database migration, similarity search, graph analytics, and community detection. Each project showcases different big data technologies and analytical techniques.

## 🎯 Projects Summary

### 1. [University Database Migration Project](./university-db-migration/README.md)
**Technologies**: PostgreSQL, MongoDB, Apache Spark  
**Objective**: Migrate a traditional RDBMS to NoSQL and perform analytics

- Transform relational university database to document-based MongoDB
- Implement ETL pipeline for data migration
- Execute complex queries using Apache Spark
- Performance optimization and comparative analysis
[📁 View Project](./University%20Database%20Migration%20Project/)
[📖 Detailed README](./University%20Database%20Migration%20Project/README.md)

---

### 2. [LSH Text Similarity Finder](./lsh-text-similarity/README.md)
**Technologies**: Python, Locality Sensitive Hashing, MinHash  
**Objective**: Find similar text documents efficiently using LSH

- Implement LSH for high-dimensional text data
- Retrieve top-5 most similar documents
- Evaluate performance with intersection scores
- Statistical analysis and visualization

[📁 View Project](./lsh-text-similarity/) | [📖 Detailed README](./lsh-text-similarity/README.md)

---

### 3. [Citation SimRank Analysis](./citation-simrank-analysis/README.md)
**Technologies**: Neo4j, Apache Spark, GraphX  
**Objective**: Find similar papers in citation networks using SimRank

- Build citation graph in Neo4j
- Implement SimRank algorithm with Spark
- Compare results with different decay factors (C = 0.7, 0.8, 0.9)
- Analyze similarity for query nodes

[📁 View Project](./citation-simrank-analysis/) | [📖 Detailed README](./citation-simrank-analysis/README.md)

---

### 4. [AGM Community Detection](./agm-community-detection/README.md)
**Technologies**: Apache Spark GraphX, Python/Scala  
**Objective**: Detect overlapping communities in GitHub social network

- Implement Affiliation Graph Model (AGM)
- Process large-scale social network data
- Evaluate communities using modularity
- Analyze community structure and overlaps

[📁 View Project](./agm-community-detection/) | [📖 Detailed README](./agm-community-detection/README.md)

---

## 🛠️ Technology Stack Overview

| Technology | Project 1 | Project 2 | Project 3 | Project 4 |
|------------|-----------|-----------|-----------|-----------|
| **Apache Spark** | ✅ | ❌ | ✅ | ✅ |
| **MongoDB** | ✅ | ❌ | ❌ | ❌ |
| **Neo4j** | ❌ | ❌ | ✅ | ❌ |
| **PostgreSQL** | ✅ | ❌ | ❌ | ❌ |
| **Python** | ✅ | ✅ | ✅ | ✅ |
| **GraphX** | ❌ | ❌ | ❌ | ✅ |
| **LSH/MinHash** | ❌ | ✅ | ❌ | ❌ |

## 📊 Key Learning Outcomes

### Database Technologies
- **Relational to NoSQL Migration**: Understanding schema transformation and ETL processes
- **Graph Databases**: Working with Neo4j for network data
- **Document Stores**: Leveraging MongoDB's flexibility

### Big Data Processing
- **Apache Spark**: Distributed computing for large-scale analytics
- **GraphX**: Graph-parallel computation framework
- **Performance Optimization**: Query optimization, indexing, and caching strategies

### Algorithms & Analytics
- **Locality Sensitive Hashing**: Efficient similarity search in high dimensions
- **SimRank**: Graph-based similarity measurement
- **Affiliation Graph Model**: Overlapping community detection
- **Evaluation Metrics**: Modularity, intersection scores, performance analysis

## 📁 Repository Structure

```
big-data-analytics/
│
├── university-db-migration/      # Project 1: RDBMS to MongoDB
│   ├── migration/               # ETL scripts
│   ├── spark/                   # Spark queries
│   └── README.md               
│
├── lsh-text-similarity/         # Project 2: LSH Implementation
│   ├── src/                    # Core LSH algorithms
│   ├── results/                # Evaluation results
│   └── README.md               
│
├── citation-simrank-analysis/   # Project 3: SimRank on Citations
│   ├── neo4j/                  # Graph construction
│   ├── spark/                  # SimRank implementation
│   └── README.md               
│
├── agm-community-detection/     # Project 4: AGM Communities
│   ├── spark_jobs/             # GraphX implementation
│   ├── results/                # Community detection results
│   └── README.md               
│
└── README.md                   # This file
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Java 8 or 11 (for Spark)
- Docker (optional, for databases)

### General Setup
```bash
# Clone the repository
git clone <repository-url>
cd big-data-analytics

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install common dependencies
pip install pyspark pandas numpy matplotlib seaborn jupyter
```

### Project-Specific Setup
Navigate to each project directory and follow the individual README instructions for detailed setup and execution steps.

## 📈 Performance Highlights

| Project | Dataset Size | Processing Time | Key Metric |
|---------|--------------|-----------------|------------|
| University Migration | ~100K records | < 5 minutes | Query optimization: 3x speedup |
| LSH Similarity | ~10K documents | < 2 minutes | Avg intersection score: 3.4/5 |
| Citation SimRank | 37K nodes, 289K edges | < 10 minutes | Convergence in ~8 iterations |
| AGM Communities | 37K nodes, 289K edges | < 15 minutes | Modularity: 0.42 |

## 📋 Submission Guidelines

Each project includes:
1. **Source Code**: Well-documented implementation
2. **Results**: Output files and performance metrics
3. **Reports**: Detailed analysis and findings
4. **Documentation**: README and usage instructions

## 📚 References

### Datasets
- [SNAP Stanford Network Analysis](https://snap.stanford.edu/data/)
- University sample data (provided by instructor)

### Key Papers
- [MinHash and LSH](http://infolab.stanford.edu/~ullman/mmds/ch3.pdf)
- [SimRank: A Measure of Structural-Context Similarity](https://www-cs.stanford.edu/~glenj/simrank.pdf)
- [Detecting Overlapping Communities: AGM](http://www.cs.cornell.edu/home/kleinber/icml12-agm.pdf)

### Documentation
- [Apache Spark](https://spark.apache.org/docs/latest/)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)
- [MongoDB Manual](https://docs.mongodb.com/manual/)

## 📧 Contact

For questions about these projects:
- Email: [dikshant22176@iiitd.ac.in]
- Course: Big Data Analytics
- Instructor: [Vikram Goyal]

---

## ⭐ Acknowledgments

Special thanks to the Big Data Analytics course instructors and teaching assistants for their guidance throughout these projects.

### License

These projects are submitted as part of academic coursework. Please refer to your institution's academic integrity policies regarding code reuse.
