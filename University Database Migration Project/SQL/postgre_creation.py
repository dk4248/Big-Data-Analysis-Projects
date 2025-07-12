import psycopg2

# Connect to the PostgreSQL server
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="College_DB",  # Replace with your DB name
            user="postgres",  # Replace with your username
            password="106342",  # Replace with your password
            host="localhost",  # Change if using a different host
            port="5432"  # Change if using a different port
        )
        conn.autocommit = True
        print("Connection successful!")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")

# Create the schema (Tables and Data)
def create_schema_and_insert_data(conn):
    try:
        cur = conn.cursor()

        # Create Departments table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        ''')

        # Create Instructors table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Instructors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department_id INT REFERENCES Departments(id)
            );
        ''')

        # Create Students table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department_id INT REFERENCES Departments(id),
                student_type VARCHAR(10) CHECK (student_type IN ('BTech', 'MTech', 'PhD'))
            );
        ''')

        # Create Courses table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Courses (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department_id INT REFERENCES Departments(id),
                instructor_id INT REFERENCES Instructors(id),
                is_core BOOLEAN DEFAULT FALSE
            );
        ''')

        # Create Enrollments table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Enrollments (
                id SERIAL PRIMARY KEY,
                student_id INT REFERENCES Students(id),
                course_id INT REFERENCES Courses(id),
                enrollment_date DATE NOT NULL
            );
        ''')

        # Insert data into Departments
        cur.execute('''
            INSERT INTO Departments (name) VALUES 
            ('Computer Science'), 
            ('Electronics'), 
            ('Mechanical')
            ON CONFLICT DO NOTHING;
        ''')

        # Insert data into Instructors
        cur.execute('''
            INSERT INTO Instructors (name, department_id) VALUES 
            ('Ravi Sharma', 1),
            ('Anita Desai', 1),
            ('Rahul Gupta', 2),
            ('Sneha Reddy', 3)
            ON CONFLICT DO NOTHING;
        ''')

        # Insert data into Students
        cur.execute('''
            INSERT INTO Students (name, department_id, student_type) VALUES 
            ('Arjun Patil', 1, 'BTech'),
            ('Priya Singh', 1, 'BTech'),
            ('Kiran Mehta', 2, 'MTech'),
            ('Vikram Reddy', 3, 'PhD'),
            ('Neha Iyer', 1, 'BTech')
            ON CONFLICT DO NOTHING;
        ''')

        # Insert data into Courses
        cur.execute('''
            INSERT INTO Courses (name, department_id, instructor_id, is_core) VALUES 
            ('Data Structures', 1, 1, TRUE),
            ('Algorithms', 1, 1, TRUE),
            ('Circuit Analysis', 2, 3, FALSE),
            ('Thermodynamics', 3, 4, FALSE),
            ('Database Systems', 1, 2, TRUE)
            ON CONFLICT DO NOTHING;
        ''')

        # Insert data into Enrollments
        cur.execute('''
            INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES 
            (1, 1, '2023-01-15'),
            (1, 2, '2023-01-16'),
            (2, 1, '2023-01-17'),
            (3, 3, '2023-01-18'),
            (4, 4, '2023-01-19'),
            (5, 1, '2023-01-20'),
            (5, 2, '2023-01-21'),
            (1, 5, '2023-01-22')
            ON CONFLICT DO NOTHING;
        ''')

        # Commit and close
        cur.close()
        print("Tables created and data inserted successfully!")
    except Exception as e:
        print(f"Error creating schema or inserting data: {e}")

# Main logic
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_schema_and_insert_data(conn)
        conn.close()
