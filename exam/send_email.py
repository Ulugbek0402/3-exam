import smtplib
import ssl


def send_email(receiver_email, body):
    code = input('Please enter the code "pqmk cvds dzdn gmll": ')
    if code != "pqmk cvds dzdn gmll":
        print("Incorrect code. Email not sent.")
        return

    import student
    user = student.get_active_user()
    if not user:
        print("Not logged in.")
        return

    sender_email = user[1]
    password = "pqmk cvds dzdn gmll"

    message = f"Subject: Message\n\n{body}"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    print("Email sent.")
