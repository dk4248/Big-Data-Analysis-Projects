import os
import time
from pymongo import MongoClient

# Connect to MongoDB server
def create_connection():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['College_DB']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Function to execute a query and return results
def execute_and_analyze_query(db, query_func):
    try:
        start_time = time.time()  # Start time
        results = query_func(db)
        end_time = time.time()  # End time
        execution_time = end_time - start_time  # Calculate execution time
        return f"Query executed successfully in {execution_time:.8f} seconds", results
    except Exception as e:
        print(f"Error executing query: {e}")
        return "Error", []

# Define the query functions
def fetch_students_in_course(db):
    return list(db.Students.aggregate([
        {
            "$lookup": {
                "from": "Enrollments",
                "localField": "_id",
                "foreignField": "student_id",
                "as": "enrollment"
            }
        },
        {
            "$unwind": "$enrollment"
        },
        {
            "$lookup": {
                "from": "Courses",
                "localField": "enrollment.course_id",
                "foreignField": "_id",
                "as": "course"
            }
        },
        {
            "$unwind": "$course"
        },
        {
            "$match": {
                "course.name": "Data Structures"
            }
        },
        {
            "$project": {
                "name": 1,
                "student_type": 1
            }
        }
    ]))

def average_students_per_instructor(db):
    return list(db.Courses.aggregate([
        {
            "$lookup": {
                "from": "Enrollments",
                "localField": "_id",
                "foreignField": "course_id",
                "as": "enrollment"
            }
        },
        {
            "$group": {
                "_id": "$instructor_id",
                "enrollment_count": {"$sum": {"$size": {"$ifNull": ["$enrollment", []]}}}
            }
        },
        {
            "$group": {
                "_id": None,
                "average": {"$avg": "$enrollment_count"}
            }
        }
    ]))

def list_courses_by_department(db):
    return list(db.Courses.aggregate([
        {
            "$lookup": {
                "from": "Departments",
                "localField": "department_id",
                "foreignField": "_id",
                "as": "department"
            }
        },
        {
            "$unwind": "$department"
        },
        {
            "$match": {
                "department.name": "Computer Science"
            }
        },
        {
            "$project": {
                "name": 1
            }
        }
    ]))

def total_students_per_department(db):
    return list(db.Students.aggregate([
        {
            "$lookup": {
                "from": "Departments",
                "localField": "department_id",
                "foreignField": "_id",
                "as": "department"
            }
        },
        {
            "$unwind": "$department"
        },
        {
            "$group": {
                "_id": "department.name",
                "total_students": {"$sum": 1}
            }
        }
    ]))

def instructors_taught_btech_cse_core(db):
    return list(db.Instructors.aggregate([
        {
            "$lookup": {
                "from": "Courses",
                "localField": "_id",
                "foreignField": "instructor_id",
                "as": "courses"
            }
        },
        {
            "$unwind": "$courses"
        },
        {
            "$match": {
                "courses.is_core": True,
                "courses.department_id": db.Departments.find_one({"name": "Computer Science"})["_id"]
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": db.Courses.count_documents({"is_core": True, "department_id": db.Departments.find_one({"name": "Computer Science"})["_id"]})
            }
        }
    ]))

def top_courses_by_enrollment(db):
    return list(db.Courses.aggregate([
        {
            "$lookup": {
                "from": "Enrollments",
                "localField": "_id",
                "foreignField": "course_id",
                "as": "enrollment"
            }
        },
        {
            "$project": {
                "name": 1,
                "total_enrollments": {"$size": {"$ifNull": ["$enrollment", []]}}
            }
        },
        {
            "$sort": {"total_enrollments": -1}
        },
        {
            "$limit": 10
        }
    ]))

# Create output folder
output_folder = "query_performance_analysis"
os.makedirs(output_folder, exist_ok=True)

# Main logic
if __name__ == "__main__":
    db = create_connection()
    if db is not None:
        query_functions = {
            "Fetch all students in a specific course": fetch_students_in_course,
            "Average students per instructor": average_students_per_instructor,
            "List all courses by department": list_courses_by_department,
            "Total number of students per department": total_students_per_department,
            "Instructors who taught all BTech CSE core courses": instructors_taught_btech_cse_core,
            "Top-10 courses by highest enrollments": top_courses_by_enrollment
        }
        
        for description, query_func in query_functions.items():
            performance, results = execute_and_analyze_query(db, query_func)

            # Save performance and results to separate text files
            result_filename = os.path.join(output_folder, f"{description.replace(' ', '_').replace(':', '')}.txt")
            with open(result_filename, 'w') as result_file:
                result_file.write(f"--- Results for: {description} ---\n")
                for result in results:
                    result_file.write(f"{result}\n")
                result_file.write("\n--- Performance Analysis ---\n")
                result_file.write(f"{performance}\n")

        print(f"Query performance analysis saved in folder: {output_folder}")
