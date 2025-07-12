from neo4j import GraphDatabase
from tqdm import tqdm
import json


# Function to clear the database
def clear_database(tx):
    tx.run("MATCH (n) DETACH DELETE n")

# Function to create a paper node
def create_paper_node(tx, paper_id):
    query = """
    MERGE (p:Paper {id: $paper_id})
    """
    tx.run(query, paper_id=paper_id)

# Function to create a cites relationship
def create_cites_relationship(tx, citing_paper_id, cited_paper_id):
    query = """
    MATCH (a:Paper {id: $citing_paper_id})
    MATCH (b:Paper {id: $cited_paper_id})
    MERGE (a)-[:CITES]->(b)
    """
    tx.run(query, citing_paper_id=citing_paper_id, cited_paper_id=cited_paper_id)

def train():

    # Step 1: Initialize Neo4j connection with updated authentication
    uri = "bolt://localhost:7687"  # Adjust as needed for your setup
    username = "neo4j"              # Replace with your actual Neo4j username
    password = "dkak1063"           # Replace with your actual Neo4j password

    # Initialize the driver with updated authentication
    driver = GraphDatabase.driver(uri, auth=(username, password))
# Read data from JSON file
    data = []
    with open('train.json') as f:
        for line in f:
            data.append(json.loads(line))

    # randomly sample 10% of the data
    import random
    data = random.sample(data, int(len(data)*0.1))

    # data = data[:100]  # Limit to first 100 rows for now

    # Step 2: Clear the existing database and populate with new data
    with driver.session() as session:
        # Clear the database first
        session.execute_write(clear_database)
        
        # Add nodes and edges for each row
        for row in tqdm(data, desc="Processing rows"):
            session.execute_write(create_paper_node, row["paper"])
            
            # Create nodes and CITES relationships for each referenced paper
            for cited_paper in row["reference"]:
                session.execute_write(create_paper_node, cited_paper)
                session.execute_write(create_cites_relationship, row["paper"], cited_paper)

    # Close the driver when done
    driver.close()