# Modules
import hashlib
import random
import smtplib
import ssl
from email.message import EmailMessage

import firebase_admin
from firebase_admin import credentials, firestore

# Connection to firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
cred = firestore.client()

# Creating collections
users = cred.collection("users")
admins = cred.collection("admins")

# Email bot
sender_email = "halitsbot@gmail.com"
email_password = open("password.txt", "r").read()


class User:
    def __init__(self) -> None:
        pass

    def user_panel(self):
        print(
            f"""
            Welcome {user_name}
            To change your password press 1
            To change your email press 2
            To change your username press 3
            To logout press 4"""
        )
        user_string = input("Enter your choice:\t")
        if user_string == "1":
            return
        elif user_string == "2":
            return
        elif user_string == "3":
            return
        elif user_string == "4":
            return

    def login(self):
        global user_name
        global data
        user_name = input("Enter your username:\t")
        if users.document(user_name).get().exists == False:
            print("User could not found")
            user_name = None
            self.register()
        data = users.document(user_name).get().to_dict()
        user_email = input("Enter your email:\t")
        if user_email == data["email"]:
            user_password = input("Enter your password:\t")
            user_password = hashlib.sha256(user_password.encode()).hexdigest()
            if user_password == data["password"]:
                print("Login successful")
                users.document(user_name).update({"status": "online"})
                self.user_panel()
            else:
                print("Wrong password")
                self.login()
        else:
            print("Wrong email")
            self.login()

    def register(self):
        new_name = input("Enter your username:\t")
        if users.document(new_name).get().exists == True:
            print("Username already taken")
            self.register()
        new_email = input("Enter your email:\t")
        code = random.randint(100000, 999999)
        email_verification(new_name, new_email, code)
        user_code = input("Enter the code we sent to your email:\t")
        if user_code == code:
            new_password = input("Enter your password:\t")
            new_password = hashlib.sha256(new_password.encode()).hexdigest()
            users.document(new_name).set(
                {"email": new_email, "password": new_password, "status": "offline"}
            )
            print("Registration successful")
            self.login()

    @staticmethod
    def logout():
        users.document(user_name).update({"status": "offline"})
        print("Logout successful")

    def change_password():
        user_password = str(input("Enter your password:\t"))
        user_password = hashlib.sha256(user_password.encode()).hexdigest()
        if user_password == data["password"]:
            new_password = str(input("Enter your new password:\t"))
            password_confirm = str(input("Enter your new password again:\t"))
            if new_password == password_confirm:
                new_password = hashlib.sha256(new_password.encode()).hexdigest()
                users.document(user_name).update({"password": new_password})
                print("Password change succesfully")
            else:
                print("Passwords does not match.")
        else:
            print("Wrong password")


class Admin:
    def admin_panel(self):
        return

    def login(self):
        global admin_name
        admin_name = str(input("Enter your username:\t"))
        if admins.document(admin_name).get().exists == False:
            print("Admin coul not found")
        admin_email = str(input("Enter your email:\t"))
        data = admins.document(admin_name).get().to_dict()
        if admin_email == data["email"]:
            admin_password = str(input("Enter your password:\t"))
            admin_password = hashlib.sha256(admin_password.encode()).hexdigest()
            if admin_password == data["password"]:
                print("Login succesful")
                self.admin_panel()


# variables of current users
current_user = User()
current_admin = Admin()


# Email verification
def email_verification(user_name, user_email, code):
    body = f"""
    Hello {user_name},
    We see that you are trying to use our service.
    
    For this you need to verify yourself. You can verify yourself with the code below.
    2 Factor Authentication Code: {code}
    
    If you are not trying to use our service, please ignore this email.
    Thanks for you'r attention."""

    mail = EmailMessage()
    mail["Subject"] = "Email verification"
    mail["From"] = sender_email
    mail["To"] = user_email
    mail.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(sender_email, user_email, mail.as_string())


if __name__ == "__main__":
    print("Welcome to our system")
    print("If you want to go to user console please press 'u'")
    user_string = str(input()).upper()
    if user_string == "U":
        print("If you want to register press 'r'")
        print("If you want to login press 'l'")
        user_string = str(input()).upper()
        if user_string == "L":
            current_user.login()
        elif user_string == "R":
            current_user.register()
        else:
            print("Please enter a valid value")
    elif user_string == "A":
        current_admin.login()
    else:
        print("Please enter a valid value")
