# Student Management System (CLI-based in Python with OOP)

import json
import os

# For SMS notifications feature
from plyer import sms


# Defining the Person class
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    # Method to display person information
    def display_person_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")


# Defining the Student class
class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    # Add grade for specific subject
    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    # Enroll in a new course
    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    # Method to display student information
    def display_student_info(self):
        print("Student Information:")
        super().display_person_info()
        print(f"ID: {self.student_id}")
        print("Enrolled Courses:", ", ".join(self.courses) if self.courses else "None")
        print("Grades:", self.grades if self.grades else "No grades yet")

    # Convert student information to dictionary format for JSON serialization
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "address": self.address,
            "student_id": self.student_id,
            "grades": self.grades,
            "courses": self.courses,
        }

    # Method to create a Student object from a dictionary (class method)
    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"], data["age"], data["address"], data["student_id"])
        student.grades = data["grades"]
        student.courses = data["courses"]
        return student


# Defining the Course class
class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    # Method to add a student to the course
    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    # Method to display course information
    def display_course_info(self):
        print("Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        student_names = [student.name for student in self.students]
        print(
            "Enrolled Students:", ", ".join(student_names) if student_names else "None"
        )

    # Method to convert course information to dictionary format for JSON serialization
    def to_dict(self):
        return {
            "course_name": self.course_name,
            "course_code": self.course_code,
            "instructor": self.instructor,
            "students": [student.student_id for student in self.students],
        }

    # Method to create a Course object from a dictionary (class method)
    @classmethod
    def from_dict(cls, data, all_students):
        course = cls(data["course_name"], data["course_code"], data["instructor"])
        for student_id in data["students"]:
            student = next(
                (s for s in all_students if s.student_id == student_id), None
            )
            if student:
                course.add_student(student)
        return course


# Defining the Student Management System class
class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.data_file = "student_data.json"

    # Method to add a student
    def add_student(self):
        print("\n=== Add New Student ===")
        name = input("Enter name: ")
        age = input("Enter age: ")
        address = input("Enter address: ")
        student_id = input("Enter student ID: ")

        # Check for Student Id already exists
        if any(s.student_id == student_id for s in self.students):
            print(f"Error: Student with ID {student_id} already exists!")
            return

        student = Student(name, age, address, student_id)
        self.students.append(student)
        print(f"Student {name} (ID: {student_id}) added successfully.")

    # Method to add a course
    def add_course(self):
        print("\n=== Add New Course ===")
        course_name = input("Enter course name: ")
        course_code = input("Enter course code: ")
        instructor = input("Enter instructor name: ")

        # Check if course code already exists
        if any(c.course_code == course_code for c in self.courses):
            print(f"Error: Course with code {course_code} already exists!")
            return

        course = Course(course_name, course_code, instructor)
        self.courses.append(course)
        print(
            f"Course {course_name} (Code: {course_code}) created with instructor {instructor}."
        )

    # Method to enroll a student in a course
    def enroll_student(self):
        print("\n=== Enroll Student in Course ===")
        student_id = input("Enter student ID: ")
        course_code = input("Enter course code: ")

        student = next((s for s in self.students if s.student_id == student_id), None)
        course = next((c for c in self.courses if c.course_code == course_code), None)

        if not student:
            print(f"Error:Student with ID {student_id} not found!")
            return

        if not course:
            print(f"Error: Course with code {course_code} not found!")
            return

        # check if student is already enrolled
        if course_code in student.courses:
            print(
                f"Student {student.name} is already enrolled in {course.course_name}!"
            )
            return

        student.enroll_course(course_code)
        course.add_student(student)
        print(
            f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code})."
        )

    # Method to add a grade
    def add_grade(self):
        print("\n=== Add Grade for Student ===")
        student_id = input("Enter student ID: ")
        course_code = input("Enter course code: ")
        grade = input("Enter grade: ")

        student = next((s for s in self.students if s.student_id == student_id), None)

        if not student:
            print(f"Error: Student with ID {student_id} not found!")
            return

        # chck if student is enrolled in the course
        if course_code not in student.courses:
            print(
                f"Error: Student {student.name} is not enrolled in course {course_code}!"
            )
            return

        student.add_grade(course_code, grade)
        print(f"Grade {grade} added for {student.name} in {course_code}.")

    # Method to display student details
    def display_student_details(self):
        print("\n=== Display Student Details ===")
        student_id = input("Enter student ID: ")
        student = next((s for s in self.students if s.student_id == student_id), None)

        if not student:
            print(f"Error: Student with ID {student_id} not found!")
            return

        student.display_student_info()

    # Method to display course details
    def display_course_details(self):
        print("\n=== Display Course Details ===")
        course_code = input("Enter course code: ")
        course = next((c for c in self.courses if c.course_code == course_code), None)

        if not course:
            print(f"Error: Course with code {course_code} not found!")
            return

        course.display_course_info()

    # Method to save data
    def save_data(self):
        print("\n=== Save Data ===")
        # Here you would implement the logic to save student and course data
        data = {
            "students": [student.to_dict() for student in self.students],
            "courses": [course.to_dict() for course in self.courses],
        }

        try:
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)
            print("All student and course data saved successfully.")

        except Exception as e:
            print(f"Error saving data: {e}")

    # Method to load data
    def load_data(self):
        print("\n=== Load Data ===")

        if not os.path.exists(self.data_file):
            print("No data file found. Starting with empty system.")
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)

            # loads student
            self.students = [
                Student.from_dict(student_data) for student_data in data["students"]
            ]
            # after then load courses with references to students
            self.courses = [
                Course.from_dict(course_data, self.students)
                for course_data in data["courses"]
            ]
            print("Data loaded successfully.")

        except Exception as e:
            print(f"Error loading data: {e}")

    # Method to display the main menu
    def display_menu(self):
        print("\n" + "=" * 40)
        print("     Student Management System")
        print("=" * 40)
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")

    # Method to run the main program loop
    def run(self):
        self.load_data()  # for loading data on startup

        while True:
            self.display_menu()
            option = input("Select Option: ")

            if option == "1":
                self.add_student()
            elif option == "2":
                self.add_course()
            elif option == "3":
                self.enroll_student()
            elif option == "4":
                self.add_grade()
            elif option == "5":
                self.display_student_details()
            elif option == "6":
                self.display_course_details()
            elif option == "7":
                self.save_data()
            elif option == "8":
                self.load_data()
            elif option == "0":
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


# Entry point
if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()


# The work short description
"""

This script implements a Student Management System that allows for the management of student records, course enrollments, and grade tracking. 
It provides a command-line interface for users to interact with the system and perform various operations related to student and course management.

"""
