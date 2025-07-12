import os
import time
import psycopg2
from pymongo import MongoClient
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def create_output_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)

# Function for optimized implementation
def optimized_implementation(output_folder):
    logger.info("Starting optimized implementation...")
    # PostgreSQL connection
    pg_conn = psycopg2.connect(
        dbname='College_DB',
        user='postgres',
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

    # Create indexes for optimization
    db.Departments.create_index('name')
    db.Instructors.create_index('department_id')
    db.Students.create_index('department_id')
    db.Courses.create_index('department_id')
    db.Courses.create_index('instructor_id')
    db.Enrollments.create_index('student_id')
    db.Enrollments.create_index('course_id')

    # Fetch Departments
    pg_cursor.execute("SELECT id, name FROM Departments")
    departments = pg_cursor.fetchall()
    department_map = {}
    dept_docs = []

    for dept in departments:
        dept_docs.append({"name": dept[1]})

    # Bulk insert Departments
    if dept_docs:
        result = db.Departments.insert_many(dept_docs)
        department_map = {dept[0]: result.inserted_ids[i] for i, dept in enumerate(departments)}

    # Fetch Instructors
    pg_cursor.execute("SELECT id, name, department_id FROM Instructors")
    instructors = pg_cursor.fetchall()
    instructor_map = {}
    inst_docs = []

    for inst in instructors:
        inst_docs.append({
            "name": inst[1],
            "department_id": department_map[inst[2]]
        })

    # Bulk insert Instructors
    if inst_docs:
        result = db.Instructors.insert_many(inst_docs)
        instructor_map = {inst[0]: result.inserted_ids[i] for i, inst in enumerate(instructors)}

    # Fetch Students
    pg_cursor.execute("SELECT id, name, department_id, student_type FROM Students")
    students = pg_cursor.fetchall()
    student_map = {}
    student_docs = []

    for student in students:
        student_docs.append({
            "name": student[1],
            "department_id": department_map[student[2]],
            "student_type": student[3]
        })

    # Bulk insert Students
    if student_docs:
        result = db.Students.insert_many(student_docs)
        student_map = {student[0]: result.inserted_ids[i] for i, student in enumerate(students)}

    # Fetch Courses
    pg_cursor.execute("SELECT id, name, department_id, instructor_id, is_core FROM Courses")
    courses = pg_cursor.fetchall()
    course_map = {}
    course_docs = []

    for course in courses:
        course_docs.append({
            "name": course[1],
            "department_id": department_map[course[2]],
            "instructor_id": instructor_map[course[3]],
            "is_core": course[4]
        })

    # Bulk insert Courses
    if course_docs:
        result = db.Courses.insert_many(course_docs)
        course_map = {course[0]: result.inserted_ids[i] for i, course in enumerate(courses)}

    # Fetch Enrollments
    pg_cursor.execute("SELECT id, student_id, course_id, enrollment_date FROM Enrollments")
    enrollments = pg_cursor.fetchall()
    enrollment_docs = []

    for enrollment in enrollments:
        enrollment_docs.append({
            "student_id": student_map[enrollment[1]],
            "course_id": course_map[enrollment[2]],
            "enrollment_date": datetime.strptime(str(enrollment[3]), '%Y-%m-%d')
        })

    # Bulk insert Enrollments
    if enrollment_docs:
        db.Enrollments.insert_many(enrollment_docs)

    # Close the cursor and connection
    pg_cursor.close()
    pg_conn.close()
    logger.info("Optimized implementation completed.")

# Function for original implementation
def original_implementation(output_folder):
    logger.info("Starting original implementation...")
    # PostgreSQL connection
    pg_conn = psycopg2.connect(
        dbname='College_DB',
        user='postgres',
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
    logger.info("Original implementation completed.")

# Measure time for optimized implementation
if __name__ == "__main__":
    optimized_output_folder = "optimized_results"
    original_output_folder = "original_results"

    create_output_folder(optimized_output_folder)
    create_output_folder(original_output_folder)

    start_time_optimized = time.time()
    optimized_implementation(optimized_output_folder)
    end_time_optimized = time.time()
    optimized_duration = end_time_optimized - start_time_optimized
    logger.info(f"Optimized Implementation Time: {optimized_duration:.4f} seconds")

    start_time_original = time.time()
    original_implementation(original_output_folder)
    end_time_original = time.time()
    original_duration = end_time_original - start_time_original
    logger.info(f"Original Implementation Time: {original_duration:.4f} seconds")

    # Compare and save results
    with open(os.path.join(optimized_output_folder, "performance_comparison.txt"), 'w') as f:
        f.write("Performance Comparison\n")
        f.write(f"Optimized Implementation Time: {optimized_duration:.4f} seconds\n")
        f.write(f"Original Implementation Time: {original_duration:.4f} seconds\n")
        f.write("\nComparison Results:\n")
        if optimized_duration < original_duration:
            f.write("Optimized implementation is faster.\n")
        elif optimized_duration > original_duration:
            f.write("Original implementation is faster.\n")
        else:
            f.write("Both implementations took the same time.\n")

    logger.info("Performance comparison results saved.")

