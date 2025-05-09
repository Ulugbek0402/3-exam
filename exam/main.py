from auth import register, login, logout
from teacher import add_course, view_purchased_students, change_course_price, view_messages
from student import purchase_course, view_my_courses, send_message_menu, recharge_balance, show_balance


# Menus

def auth_menu():
    while True:
        print("1. Register\n2. Login\n3. Exit")
        c = input("Choice: ")
        if c == '1':
            register()
        elif c == '2':
            role = login()
            if role == 'TEACHER':
                teacher_menu()
            elif role == 'STUDENT':
                student_menu()
        elif c == '3':
            break
        else:
            print('Invalid.')


def teacher_menu():
    while True:
        print("""
Teacher Menu:
1. Add new course
2. View course purchases
3. Change course price
4. View messages
5. Logout
""")
        choice = input("Choice: ")
        if choice == '1':
            add_course()
        elif choice == '2':
            view_purchased_students()
        elif choice == '3':
            change_course_price()
        elif choice == '4':
            view_messages()
        elif choice == '5':
            logout()
            break
        else:
            print('Invalid.')


def student_menu():
    while True:
        print("""
Student Menu:
1. Purchase course
2. View my courses
3. Send message to teacher
4. Top up balance
5. Show balance
6. Logout
""")
        choice = input("Choice: ")
        if choice == '1':
            purchase_course()
        elif choice == '2':
            view_my_courses()
        elif choice == '3':
            send_message_menu()
        elif choice == '4':
            recharge_balance()
        elif choice == '5':
            show_balance()
        elif choice == '6':
            logout()
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    auth_menu()
