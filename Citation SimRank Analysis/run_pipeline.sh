#!/bin/bash

neo4j start && sleep 10
# Step 2: Create the Neo4j database
echo "Creating Neo4j database..."
python3 main.py

# Step 3: Mock Spark integration
echo "Fetching sample data from Neo4j..."

# Using cypher-shell to run the queries
cypher-shell -u neo4j -p dkak1063 -a bolt://localhost:7687 "MATCH (p:Paper) RETURN p LIMIT 10;"
cypher-shell -u neo4j -p dkak1063 -a bolt://localhost:7687 "MATCH (p1:Paper)-[:CITES]->(p2:Paper) RETURN p1, p2 LIMIT 10;"

# Step 4: Compute SimRank
echo "Running SimRank computations..."
python3 simrank.py
