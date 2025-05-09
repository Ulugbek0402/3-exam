from file_manager import read, write
from utils import generate_id
from auth import get_active_user


def add_course():
    title = input("Enter course title: ")
    description = input("Enter course description: ")
    price = input("Enter course price: ")
    courses = read("courses.csv")
    new_id = str(generate_id("courses.csv"))
    teacher_id = get_active_user()[0]
    write("courses.csv", [new_id, title, description, price, teacher_id], mode="a")
    print("Course added.")


# Displays students who purchased the teacher's courses

def view_purchased_students():
    purchases = read("purchases.csv")
    courses = read("courses.csv")
    users = read("users.csv")
    teacher_id = get_active_user()[0]
    my_courses = [c for c in courses if c[4] == teacher_id]
    for course in my_courses:
        print(f"Course {course[0]}: {course[1]}")
        buyers = [p for p in purchases if p[1] == course[0]]
        if not buyers:
            print("  No purchases.")
        for p in buyers:
            student = next(u for u in users if u[0] == p[2])
            print(f"  - {student[1]}")


def change_course_price():
    courses = read("courses.csv")
    teacher_id = get_active_user()[0]
    my_courses = [c for c in courses if c[4] == teacher_id]
    for c in my_courses:
        print(f"{c[0]}: {c[1]} - {c[3]}")
    cid = input("Course ID to update: ")
    new_price = input("New price: ")
    for c in courses:
        if c[0] == cid and c[4] == teacher_id:
            c[3] = new_price
    write("courses.csv", courses, mode="w")
    print("Price updated.")


def view_messages():
    msgs = read("messages.csv")
    users = read("users.csv")
    teacher_id = get_active_user()[0]
    incoming = [m for m in msgs if m[2] == teacher_id]
    for m in incoming:
        sender = next(u for u in users if u[0] == m[1])
        print(f"From {sender[1]}: {m[3]}")
