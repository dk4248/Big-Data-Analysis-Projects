import psycopg2
import os

# Connect to the PostgreSQL server
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="College_DB",
            user="postgres",
            password="106342",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")

# Function to execute a query and return performance analysis
def execute_and_analyze_query(conn, query):
    try:
        cur = conn.cursor()
        # Use EXPLAIN ANALYZE to get performance details
        cur.execute(f"EXPLAIN ANALYZE {query}")
        analysis = cur.fetchall()
        
        # Execute the actual query to get results
        cur.execute(query)
        results = cur.fetchall()
        
        cur.close()
        return analysis, results
    except Exception as e:
        print(f"Error executing query: {e}")
        return [], []

# Queries to analyze
queries = {
    "Fetch all students in a specific course": """
        SELECT s.name, s.student_type 
        FROM Students s 
        JOIN Enrollments e ON s.id = e.student_id 
        JOIN Courses c ON e.course_id = c.id 
        WHERE c.name = 'Data Structures';
    """,
    "Average students per instructor": """
        SELECT AVG(enrollment_count) 
        FROM (
            SELECT COUNT(e.student_id) AS enrollment_count 
            FROM Enrollments e 
            JOIN Courses c ON e.course_id = c.id 
            JOIN Instructors i ON c.instructor_id = i.id 
            WHERE i.name = 'Ravi Sharma' 
            GROUP BY c.id
        ) AS course_counts;
    """,
    "List all courses by department": """
        SELECT c.name 
        FROM Courses c 
        JOIN Departments d ON c.department_id = d.id 
        WHERE d.name = 'Computer Science';
    """,
    "Total number of students per department": """
        SELECT d.name AS department_name, COUNT(s.id) AS total_students 
        FROM Students s 
        JOIN Departments d ON s.department_id = d.id 
        GROUP BY d.id;
    """,
    "Instructors who taught all BTech CSE core courses": """
        SELECT DISTINCT i.name 
        FROM Instructors i 
        JOIN Courses c ON i.id = c.instructor_id 
        WHERE c.is_core = TRUE 
        AND c.department_id = (SELECT MIN(id) FROM Departments WHERE name = 'Computer Science') 
        GROUP BY i.id 
        HAVING COUNT(c.id) = (
            SELECT COUNT(*) 
            FROM Courses 
            WHERE is_core = TRUE 
            AND department_id = (SELECT MIN(id) FROM Departments WHERE name = 'Computer Science')
        );
    """,
    "Top-10 courses by highest enrollments": """
        SELECT c.name, COUNT(e.student_id) AS total_enrollments 
        FROM Courses c 
        JOIN Enrollments e ON c.id = e.course_id 
        GROUP BY c.id 
        ORDER BY total_enrollments DESC 
        LIMIT 10;
    """
}

# Create output folder
output_folder = "query_performance_analysis"
os.makedirs(output_folder, exist_ok=True)

# Main logic
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        performance_results = []

        for description, query in queries.items():
            performance, results = execute_and_analyze_query(conn, query)
            performance_results.append((description, performance, results))

            # Write results to separate files
            result_filename = os.path.join(output_folder, f"{description.replace(' ', '_').replace(':', '')}.txt")
            with open(result_filename, 'w') as result_file:
                result_file.write(f"--- Results for: {description} ---\n")
                for result in results:
                    result_file.write(f"{result}\n")
                result_file.write("\n--- Performance Analysis ---\n")
                for line in performance:
                    result_file.write(f"{line}\n")

        conn.close()

        # Write all performance results to a single file
        with open(os.path.join(output_folder, "query_performance_analysis.txt"), 'w') as file:
            for description, performance, _ in performance_results:
                file.write(f"--- {description} ---\n")
                for line in performance:
                    file.write(f"{line}\n")
                file.write("\n")
        
        print(f"Query performance analysis saved in folder: {output_folder}")
