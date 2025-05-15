from file_manager import read, write
from send_email import send_email
from auth import get_active_user


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
    user = get_active_user()
    if not user:
        print("Not logged in.")
        return
    uid = str(user[0])

    courses = read("courses.csv")
    if not courses:
        print("No courses available.")
        return

    default_prices = {
        "math": "1000$",

    }

    print("Available courses:")
    for c in courses:
        title = c[1].capitalize()
        price_str = c[2].strip()

        if price_str.lower() == title.lower():
            price_str = default_prices.get(title.lower(), price_str)
        print(f"{c[0]}. {title} - {price_str}")

    course_id = input("Enter course ID to purchase: ")
    selected = next((c for c in courses if c[0] == course_id), None)
    if not selected:
        print("Invalid course ID.")
        return

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

    balances = read("balances.csv")
    bal_row = next((b for b in balances if b[0] == uid), None)
    balance = float(bal_row[1]) if bal_row else 0.0
    if balance < price:
        print(f"Insufficient balance (have {balance}, need {price}). Please top up.")
        return

    new_balance = balance - price
    if bal_row:
        bal_row[1] = str(new_balance)
    else:
        balances.append([uid, str(new_balance)])
    write("balances.csv", balances)

    purchases = read("purchases.csv")
    purchases.append([uid, course_id])
    write("purchases.csv", purchases)

    print(f"Course {selected[1].capitalize()} purchased! Remaining balance: {new_balance}")


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
    user = get_active_user()
    if not user:
        print("Not logged in.")
        return
    sid = str(user[0])

    purchases = read("purchases.csv")
    my_courses = [p for p in purchases if p[0] == sid]
    if not my_courses:
        print("You haven't purchased any courses.")
        return

    courses = read("courses.csv")

    print("Your courses:")
    for p in my_courses:
        course = next((c for c in courses if c[0] == p[1]), None)
        if course:
            print(f"{course[0]}. {course[1].capitalize()}")

    selected = input("Enter course ID to message: ")
    if selected not in [p[1] for p in my_courses]:
        print("Invalid choice.")
        return

    course = next((c for c in courses if c[0] == selected), None)
    if not course or len(course) < 4:
        print("Teacher email not found for this course.")
        return
    receiver_email = course[3]

    body = input("Type your message: ")
    send_email(receiver_email, body)


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
