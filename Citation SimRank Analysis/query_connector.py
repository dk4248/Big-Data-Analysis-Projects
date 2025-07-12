from pyspark.sql import SparkSession

def connect():
    try:
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName("Neo4j Integration") \
            .config("spark.neo4j.url", "bolt://localhost:7687") \
            .getOrCreate()
        
        print("Connection established")
        exit()

        # Query to fetch data from Neo4j
        query = "MATCH (n) RETURN n LIMIT 10"
        df = spark.read.format("neo4j").option("query", query).load()

        # Display the query result
        df.show()

    except Exception as e:
        # If there is an exception, log it and exit
        print("Connection failed.")
        # Uncomment this line to debug if needed
        # print(e)

