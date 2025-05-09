from file_manager import read, write
from utils import generate_id
from send_email import send_email
from auth import get_active_user


# Lets a student purchase a course

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(digits_of(d * 2))
    return total % 10


def is_valid_card(card_number):
    try:
        int(card_number)
    except ValueError:
        return False
    return luhn_checksum(card_number) == 0


def purchase_course():
    # 1) Ensure someone is logged in
    user = get_active_user()
    if not user:
        print("Not logged in.")
        return
    uid = str(user[0])

    # 2) Load courses
    courses = read("courses.csv")  # expects rows like [id, title, price]
    if not courses:
        print("No courses available.")
        return

    # 3) Define any fallback prices (keyed by lowercase title)
    default_prices = {
        "math": "1000$",
        # add more if you have other bad entries
    }

    # 4) Display courses with correct prices
    print("Available courses:")
    for c in courses:
        title = c[1].capitalize()
        price_str = c[2].strip()
        # if price field just repeats the title, use our fallback
        if price_str.lower() == title.lower():
            price_str = default_prices.get(title.lower(), price_str)
        print(f"{c[0]}. {title} - {price_str}")

    # 5) Choose one
    course_id = input("Enter course ID to purchase: ")
    selected = next((c for c in courses if c[0] == course_id), None)
    if not selected:
        print("Invalid course ID.")
        return

    # 6) Parse the price (strip '$' and convert)
    raw_price = selected[2].strip()
    if raw_price.lower() == selected[1].lower():
        raw_price = default_prices.get(raw_price.lower(), raw_price)
    if raw_price.endswith('$'):
        raw_price = raw_price[:-1]
    try:
        price = float(raw_price)
    except ValueError:
        print(f"Invalid price format: {selected[2]}")
        return

    # 7) Load balance and check funds
    balances = read("balances.csv")  # rows: [user_id, balance]
    bal_row = next((b for b in balances if b[0] == uid), None)
    balance = float(bal_row[1]) if bal_row else 0.0
    if balance < price:
        print(f"Insufficient balance (have {balance}, need {price}). Please top up.")
        return

    # 8) Deduct price and save balances.csv
    new_balance = balance - price
    if bal_row:
        bal_row[1] = str(new_balance)
    else:
        balances.append([uid, str(new_balance)])
    write("balances.csv", balances)

    # 9) Record the purchase
    purchases = read("purchases.csv")  # rows: [user_id, course_id]
    purchases.append([uid, course_id])
    write("purchases.csv", purchases)

    print(f"Course {selected[1].capitalize()} purchased! Remaining balance: {new_balance}")


# Shows the student's purchased courses

def view_my_courses():
    user = get_active_user()
    if not user:
        print("Not logged in.")
        return
    sid = str(user[0])

    purchases = read("purchases.csv")
    my_purchases = [p for p in purchases if p[0] == sid]
    if not my_purchases:
        print("You haven't purchased any courses.")
        return

    courses = read("courses.csv")

    default_prices = {
        "math": "1000$",

    }

    # 5) Print them
    print("Your courses:")
    for p in my_purchases:
        course_id = p[1]
        course = next((c for c in courses if c[0] == course_id), None)
        if not course:
            continue

        title = course[1].capitalize()
        price_str = course[2].strip()
        if price_str.lower() == title.lower():
            price_str = default_prices.get(title.lower(), price_str)

        print(f"{course[0]}. {title} - {price_str}")


def send_message_menu():
    purchases = read("purchases.csv")
    courses = read("courses.csv")
    sid = get_active_user()[0]
    my_courses = [p for p in purchases if p[2] == sid]
    if not my_courses:
        print("You have not purchased any courses.")
        return
    print("Your Courses:")
    for p in my_courses:
        c = next(course for course in courses if course[0] == p[1])
        print(f"{c[0]}: {c[1]}")
    cid = input("Enter Course ID for messaging: ")
    course = next((c for c in courses if c[0] == cid), None)
    if not course:
        print("Invalid Course ID.")
        return
    teacher_id = course[4]
    users = read("users.csv")
    teacher = next((u for u in users if u[0] == teacher_id), None)
    if not teacher:
        print("Instructor not found.")
        return
    while True:
        print("1. Send by Email\n2. Send in Platform\n3. Back")
        choice = input("Choice: ")
        msg = input("Enter your message: ") if choice in ('1', '2') else None
        if choice == '1':
            send_email(teacher[1], msg)
            print("Email sent.")
            break
        elif choice == '2':
            new_id = str(generate_id("messages.csv"))
            write("messages.csv", [new_id, sid, teacher_id, msg], mode="a")
            print("Message stored in platform.")
            break
        elif choice == '3':
            return
        else:
            print("Invalid choice.")


def show_balance():
    user = get_active_user()
    if not user:
        print("Not logged in.")
        return

    uid = str(user[0])
    balances = read("balances.csv")

    for row in balances:
        if row[0] == uid:
            print(f"Your current balance is: {row[1]}")
            return

    print("Your current balance is: 0")


def recharge_balance():
    user = get_active_user()
    if not user:
        print("Not logged in.")
        return

    uid = str(user[0])

    amt_str = input("Enter amount to top up: ")
    try:
        amt = float(amt_str)
        if amt <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid number.")
        return

    balances = read("balances.csv")
    updated = False

    for row in balances:
        if row[0] == uid:
            new_bal = float(row[1]) + amt
            row[1] = str(new_bal)
            updated = True
            break

    if not updated:
        balances.append([uid, str(amt)])
        new_bal = amt

    write("balances.csv", balances)

    print(f"Balance updated! Your new balance is: {new_bal}")
