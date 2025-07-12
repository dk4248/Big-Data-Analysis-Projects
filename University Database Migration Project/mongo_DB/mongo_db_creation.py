import time
import psycopg2
from pymongo import MongoClient
from datetime import datetime

def original_implementation():
    # PostgreSQL connection
    pg_conn = psycopg2.connect(
        dbname='College_DB',
        user='postgres',``
        password='106342',
        host='localhost',
        port='5432'
    )
    pg_cursor = pg_conn.cursor()

    # MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']

    # Clear existing collections
    db.Departments.delete_many({})
    db.Instructors.delete_many({})
    db.Students.delete_many({})
    db.Courses.delete_many({})
    db.Enrollments.delete_many({})

    # Fetch Departments
    pg_cursor.execute("SELECT id, name FROM Departments")
    departments = pg_cursor.fetchall()
    department_map = {}
    for dept in departments:
        dept_doc = {"name": dept[1]}
        result = db.Departments.insert_one(dept_doc)
        department_map[dept[0]] = result.inserted_id

    # Fetch Instructors
    pg_cursor.execute("SELECT id, name, department_id FROM Instructors")
    instructors = pg_cursor.fetchall()
    instructor_map = {}
    for inst in instructors:
        inst_doc = {"name": inst[1], "department_id": department_map[inst[2]]}
        result = db.Instructors.insert_one(inst_doc)
        instructor_map[inst[0]] = result.inserted_id

    # Fetch Students
    pg_cursor.execute("SELECT id, name, department_id, student_type FROM Students")
    students = pg_cursor.fetchall()
    student_map = {}
    for student in students:
        student_doc = {
            "name": student[1],
            "department_id": department_map[student[2]],
            "student_type": student[3]
        }
        result = db.Students.insert_one(student_doc)
        student_map[student[0]] = result.inserted_id

    # Fetch Courses
    pg_cursor.execute("SELECT id, name, department_id, instructor_id, is_core FROM Courses")
    courses = pg_cursor.fetchall()
    course_map = {}
    for course in courses:
        course_doc = {
            "name": course[1],
            "department_id": department_map[course[2]],
            "instructor_id": instructor_map[course[3]],
            "is_core": course[4]
        }
        result = db.Courses.insert_one(course_doc)
        course_map[course[0]] = result.inserted_id

    # Fetch Enrollments
    pg_cursor.execute("SELECT id, student_id, course_id, enrollment_date FROM Enrollments")
    enrollments = pg_cursor.fetchall()
    for enrollment in enrollments:
        enrollment_doc = {
            "student_id": student_map[enrollment[1]],
            "course_id": course_map[enrollment[2]],
            "enrollment_date": datetime.strptime(str(enrollment[3]), '%Y-%m-%d')
        }
        db.Enrollments.insert_one(enrollment_doc)

    # Close the cursor and connection
    pg_cursor.close()
    pg_conn.close()

# Measure time for original implementation
start_time_original = time.time()
original_implementation()
end_time_original = time.time()
original_duration = end_time_original - start_time_original
print(f"Original Implementation Time: {original_duration:.4f} seconds")
