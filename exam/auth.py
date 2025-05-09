from file_manager import write, read
from utils import generate_id


def is_valid_email(email: str) -> bool:
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if "." not in domain:
        return False
    return True


def register():
    global new_user
    email = input("Enter your email: ")
    if not is_valid_email(email):
        print("Invalid email format. Example: user@example.com")
        return

    password = input("Enter your password: ")
    who = input("Teacher or student?: ").strip().lower()
    if who == "teacher" or who == "student":
        new_id = generate_id(filename="users.csv")
        new_user = [new_id, email, password, who.upper(), 0]
        write(filename="users.csv", data=new_user, mode="a")
        print("User is registered")
    else:
        print("Enter only: student or teacher")
        register()


def login():
    email = input("Enter your email: ")
    if not is_valid_email(email):
        print("Invalid email format.")
        return False

    password = input("Enter your password: ")
    users = read(filename="users.csv")

    for user in users:

        if user[1] == email and user[2] == password:
            if user[3] == "STUDENT":
                user[-1] = 1
                write(filename="users.csv", data=users, mode="w")
                print("Login successful")
                return "STUDENT"
            elif user[3] == "TEACHER":
                user[-1] = 1
                write(filename="users.csv", data=users, mode="w")
                print("Login successful")
                return "TEACHER"

    print("Email or password is incorrect.")
    return False


def logout():
    data = read(filename="users.csv")
    for index in range(len(data)):
        data[index][-1] = 0
        write(filename="users.csv", data=data)


def get_active_user():
    users = read(filename="users.csv")
    for user in users:
        if user[-1] == "1":
            return user
