import time
from pymongo import MongoClient

# Original Query Implementations

def fetch_students_in_course_original(course_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    students = list(db.Enrollments.find({"course_id": course_id}, {"student_id": 1}))
    end_time = time.time()
    
    performance = end_time - start_time
    return students, performance

def avg_students_per_instructor_original(instructor_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    total_students = db.Enrollments.count_documents({
        "course_id": {
            "$in": list(db.Courses.find({"instructor_id": instructor_id}, {"_id": 1}))
        }
    })
    total_courses = db.Courses.count_documents({"instructor_id": instructor_id})
    avg_count = total_students / total_courses if total_courses > 0 else 0
    end_time = time.time()
    
    performance = end_time - start_time
    return avg_count, performance

def courses_by_department_original(department_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    courses = list(db.Courses.find({"department_id": department_id}, {"name": 1}))
    end_time = time.time()
    
    performance = end_time - start_time
    return courses, performance

def total_students_per_department_original():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    total_count = list(db.Students.aggregate([
        {
            "$group": {
                "_id": "$department_id",
                "total_students": {"$sum": 1}
            }
        }
    ]))
    end_time = time.time()
    
    performance = end_time - start_time
    return total_count, performance

def instructors_teaching_btech_cse_core_original():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    instructors = list(db.Courses.find({
        "is_core": True,
        "department_id": "BTech_CSE"  # Replace with actual department_id if needed
    }))
    end_time = time.time()
    
    performance = end_time - start_time
    return instructors, performance

def top_courses_by_enrollment_original():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    top_courses = list(db.Enrollments.aggregate([
        {
            "$group": {
                "_id": "$course_id",
                "enrollment_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"enrollment_count": -1}
        },
        {
            "$limit": 10
        }
    ]))
    end_time = time.time()
    
    performance = end_time - start_time
    return top_courses, performance

# Optimized Query Implementations
def fetch_students_in_course(course_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    students = list(db.Enrollments.aggregate([
        {
            "$match": {"course_id": course_id}
        },
        {
            "$lookup": {
                "from": "Students",
                "localField": "student_id",
                "foreignField": "_id",
                "as": "student_info"
            }
        },
        {
            "$unwind": "$student_info"
        },
        {
            "$project": {
                "student_name": "$student_info.name"
            }
        }
    ]))
    end_time = time.time()
    
    performance = end_time - start_time
    return students, performance


def avg_students_per_instructor(instructor_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    avg_count = db.Enrollments.aggregate([
        {
            "$lookup": {
                "from": "Courses",
                "localField": "course_id",
                "foreignField": "_id",
                "as": "course_info"
            }
        },
        {
            "$match": {"course_info.instructor_id": instructor_id}
        },
        {
            "$group": {
                "_id": "$course_id",
                "student_count": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": None,
                "avg_students": {"$avg": "$student_count"}
            }
        }
    ])
    
    result = list(avg_count)
    end_time = time.time()
    
    performance = end_time - start_time
    return result[0]['avg_students'] if result else 0, performance


def courses_by_department(department_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    courses = list(db.Courses.find({"department_id": department_id}, {"name": 1}))
    end_time = time.time()
    
    performance = end_time - start_time
    return courses, performance


def total_students_per_department():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    total_count = list(db.Students.aggregate([
        {
            "$lookup": {
                "from": "Departments",
                "localField": "department_id",
                "foreignField": "_id",
                "as": "department_info"
            }
        },
        {
            "$group": {
                "_id": "$department_id",
                "total_students": {"$sum": 1}
            }
        }
    ]))
    end_time = time.time()
    
    performance = end_time - start_time
    return total_count, performance


def instructors_teaching_btech_cse_core():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    instructors = list(db.Courses.aggregate([
        {
            "$match": {
                "is_core": True,
                "department_id": "BTech_CSE"  # Replace with actual department_id if needed
            }
        },
        {
            "$group": {
                "_id": "$instructor_id",
                "courses_taught": {"$addToSet": "$name"}
            }
        },
        {
            "$match": {
                "$expr": {
                    "$eq": [{"$size": "$courses_taught"}, 6]  # Assuming 6 core courses
                }
            }
        }
    ]))
    end_time = time.time()
    
    performance = end_time - start_time
    return instructors, performance


def top_courses_by_enrollment():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['College_DB']
    
    start_time = time.time()
    top_courses = list(db.Enrollments.aggregate([
        {
            "$group": {
                "_id": "$course_id",
                "enrollment_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"enrollment_count": -1}
        },
        {
            "$limit": 10
        },
        {
            "$lookup": {
                "from": "Courses",
                "localField": "_id",
                "foreignField": "_id",
                "as": "course_info"
            }
        }
    ]))
    end_time = time.time()
    
    performance = end_time - start_time
    return top_courses, performance


# Function to run both optimized and original queries and save results
def run_queries_and_save_results():
    results = []
    performances = []

    # Example course_id, instructor_id, and department_id to replace with actual values
    course_id = "YOUR_COURSE_ID_HERE"  
    instructor_id = "YOUR_INSTRUCTOR_ID_HERE"  
    department_id = "YOUR_DEPARTMENT_ID_HERE"  

    # Fetching all students enrolled in a specific course
    students_original, performance_original = fetch_students_in_course_original(course_id)
    students_optimized, performance_optimized = fetch_students_in_course(course_id)
    results.append(f"Original Students in Course {course_id}: {students_original}")
    results.append(f"Optimized Students in Course {course_id}: {students_optimized}")
    performances.append(f"Original Time for Fetching Students in Course: {performance_original:.4f} seconds")
    performances.append(f"Optimized Time for Fetching Students in Course: {performance_optimized:.4f} seconds")

    # Calculating the average number of students enrolled in courses offered by a particular instructor
    avg_students_original, performance_original = avg_students_per_instructor_original(instructor_id)
    avg_students_optimized, performance_optimized = avg_students_per_instructor(instructor_id)
    results.append(f"Original Average Students per Instructor {instructor_id}: {avg_students_original}")
    results.append(f"Optimized Average Students per Instructor {instructor_id}: {avg_students_optimized}")
    performances.append(f"Original Time for Average Students per Instructor: {performance_original:.4f} seconds")
    performances.append(f"Optimized Time for Average Students per Instructor: {performance_optimized:.4f} seconds")

    # Listing all courses offered by a specific department
    courses_original, performance_original = courses_by_department_original(department_id)
    courses_optimized, performance_optimized = courses_by_department(department_id)
    results.append(f"Original Courses in Department {department_id}: {courses_original}")
    results.append(f"Optimized Courses in Department {department_id}: {courses_optimized}")
    performances.append(f"Original Time for Courses by Department: {performance_original:.4f} seconds")
    performances.append(f"Optimized Time for Courses by Department: {performance_optimized:.4f} seconds")

    # Finding total number of students per department
    total_students_original, performance_original = total_students_per_department_original()
    total_students_optimized, performance_optimized = total_students_per_department()
    results.append(f"Original Total Students per Department: {total_students_original}")
    results.append(f"Optimized Total Students per Department: {total_students_optimized}")
    performances.append(f"Original Time for Total Students per Department: {performance_original:.4f} seconds")
    performances.append(f"Optimized Time for Total Students per Department: {performance_optimized:.4f} seconds")

    # Finding instructors who have taught all the BTech CSE core courses
    instructors_original, performance_original = instructors_teaching_btech_cse_core_original()
    instructors_optimized, performance_optimized = instructors_teaching_btech_cse_core()
    results.append(f"Original Instructors who taught all BTech CSE Core Courses: {instructors_original}")
    results.append(f"Optimized Instructors who taught all BTech CSE Core Courses: {instructors_optimized}")
    performances.append(f"Original Time for Instructors Teaching BTech CSE Core Courses: {performance_original:.4f} seconds")
    performances.append(f"Optimized Time for Instructors Teaching BTech CSE Core Courses: {performance_optimized:.4f} seconds")

    # Finding top-10 courses with the highest enrollments
    top_courses_original, performance_original = top_courses_by_enrollment_original()
    top_courses_optimized, performance_optimized = top_courses_by_enrollment()
    results.append(f"Original Top-10 Courses with Highest Enrollments: {top_courses_original}")
    results.append(f"Optimized Top-10 Courses with Highest Enrollments: {top_courses_optimized}")
    performances.append(f"Original Time for Top-10 Courses by Enrollment: {performance_original:.4f} seconds")
    performances.append(f"Optimized Time for Top-10 Courses by Enrollment: {performance_optimized:.4f} seconds")

    # Save results to a text file
    with open("query_results_comparison.txt", "w") as result_file:
        for result in results:
            result_file.write(result + "\n")

    # Save performance analysis to a different text file
    with open("performance_analysis_comparison.txt", "w") as performance_file:
        for analysis in performances:
            performance_file.write(analysis + "\n")

# Run the function to execute queries and save results
run_queries_and_save_results()
