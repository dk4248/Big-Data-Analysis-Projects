# University Database Migration Project

## RDBMS to MongoDB Migration with Apache Spark Analytics

### Course: Big Data Analytics | Assignment-1

---

## 📋 Project Overview

This project demonstrates the migration of a traditional university student information system from PostgreSQL (RDBMS) to MongoDB (NoSQL), with query implementation and performance analysis using Apache Spark. The project showcases modern data engineering practices including ETL processes, schema transformation, and distributed computing.

## 🎯 Objectives

1. **Data Modeling**: Transform relational schema to document-based MongoDB schema
2. **Data Migration**: Implement ETL pipeline for PostgreSQL to MongoDB migration
3. **Query Implementation**: Execute complex queries using Apache Spark on MongoDB
4. **Performance Optimization**: Analyze and optimize query performance

## 🛠️ Technology Stack

- **Source Database**: PostgreSQL
- **Target Database**: MongoDB
- **Processing Framework**: Apache Spark
- **Programming Languages**: Python/Scala
- **Additional Tools**: 
  - MongoDB Connector for Spark
  - PySpark/Spark SQL
  - Jupyter Notebooks (for development)

## 📁 Project Structure

```
university-db-migration/
│
├── data/
│   ├── postgresql_schema.sql      # Original RDBMS schema
│   └── sample_data/               # Sample data files
│
├── migration/
│   ├── etl_pipeline.py           # Main ETL script
│   ├── data_validator.py         # Data validation utilities
│   └── config/                   # Database configurations
│
├── mongodb/
│   ├── schema_design.json        # MongoDB schema design
│   └── indexes.js                # Index creation scripts
│
├── spark/
│   ├── query_implementations/    # Spark query scripts
│   │   ├── q1_students_by_course.py
│   │   ├── q2_avg_students_by_instructor.py
│   │   ├── q3_courses_by_department.py
│   │   ├── q4_students_per_department.py
│   │   ├── q5_instructors_all_core_courses.py
│   │   └── q6_top10_enrolled_courses.py
│   │
│   └── optimization/             # Performance optimization scripts
│
├── reports/
│   ├── schema_mapping_report.pdf
│   ├── migration_report.pdf
│   ├── query_results_report.pdf
│   └── performance_analysis_report.pdf
│
├── notebooks/
│   └── analysis.ipynb            # Jupyter notebook for analysis
│
├── docs/
│   └── presentation.pptx         # Project presentation
│
└── README.md                     # This file
```

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- MongoDB 4.4+
- Apache Spark 3.0+
- Java 8 or 11

### Required Python Packages
```bash
pip install psycopg2-binary
pip install pymongo
pip install pyspark
pip install pandas
pip install numpy
```

## 🚀 Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd university-db-migration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

#### PostgreSQL Setup
```bash
# Create database
createdb university_db

# Load schema and sample data
psql -d university_db -f data/postgresql_schema.sql
psql -d university_db -f data/sample_data.sql
```

#### MongoDB Setup
```bash
# Start MongoDB service
mongod --dbpath /path/to/data

# Create database and collections
mongo university_nosql --eval "db.createCollection('students')"
```

### 3. Spark Configuration

```bash
# Set Spark environment variables
export SPARK_HOME=/path/to/spark
export PATH=$SPARK_HOME/bin:$PATH

# Download MongoDB Spark Connector
wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.1/mongo-spark-connector_2.12-3.0.1.jar
```

## 📊 Query Workload

The following queries are implemented:

1. **Q1**: Fetch all students enrolled in a specific course
2. **Q2**: Calculate average students per instructor
3. **Q3**: List all courses by department
4. **Q4**: Find total students per department
5. **Q5**: Find instructors who taught all BTech CSE core courses
6. **Q6**: Find top-10 courses by enrollment

## 🏃 Running the Project

### 1. Data Migration

```bash
# Run the ETL pipeline
python migration/etl_pipeline.py --config migration/config/db_config.json

# Validate migrated data
python migration/data_validator.py
```

### 2. Execute Queries

```bash
# Run individual queries
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    spark/query_implementations/q1_students_by_course.py

# Run all queries
bash scripts/run_all_queries.sh
```

### 3. Performance Analysis

```bash
# Run performance benchmarks
python spark/optimization/benchmark.py

# Generate performance report
python spark/optimization/generate_report.py
```

## 📈 Deliverables

1. **Schema Mapping Report** (`reports/schema_mapping_report.pdf`)
   - Relational to document model transformation
   - Design justifications
   - Denormalization strategies

2. **Migration Scripts** (`migration/`)
   - ETL pipeline implementation
   - Data validation tools
   - Migration logs

3. **Query Implementation** (`spark/query_implementations/`)
   - All 6 queries implemented in Spark
   - Query results and analysis

4. **Performance Analysis** (`reports/performance_analysis_report.pdf`)
   - Query execution times
   - Optimization strategies
   - Before/after comparisons

## 🔧 Optimization Strategies Implemented

1. **MongoDB Indexing**
   - Compound indexes for frequent query patterns
   - Text indexes for search operations

2. **Spark Optimizations**
   - Query plan optimization
   - Data partitioning strategies
   - Broadcast joins for small tables

## 📝 Notes

- Ensure all database connections are properly configured in `config/` files
- Sample data is provided for testing; actual university data should be used for final submission
- Performance metrics may vary based on hardware specifications

---

### Contact

For questions or issues, please contact: [dikshant22176@iiitd.ac.in]
