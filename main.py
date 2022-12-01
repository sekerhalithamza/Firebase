#firebase modules for database
import firebase_admin
from firebase_admin import credentials, firestore

#hashlib module for sha-256 encoding
import hashlib

#smtplib module for sending email
import smtplib

#random module for creating random number
import random

#firebase connection
db = credentials.Certificate("./sign-up-sign-in-python-firebase-adminsdk-8kbfq-e0afe42a03.json")
app = firebase_admin.initialize_app(db)
db = firestore.client()

#creating a collection in firebase firestore database
my_document = db.collection("users")

#logging into email
sender_email = "halitsbot"
email_password = "rbflhssxgdwsbgkg"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, email_password)

#login function
def login():
    my_name = str(input("Name :\t"))
    yn = str(input("Did you forget your password? (y/n):\t"))
    if yn == "y":
        change_password()
    elif yn == "n":
        my_password = str(input("Password :\t"))
        hashed_my_password = hashlib.sha256(my_password.encode()).hexdigest()
        try:
            data = my_document.document(my_name).get().to_dict()
            data["password"]
        except KeyError:
            print('Account not found')
        except AttributeError:
            print("Account not found")
        else: 
            if data["password"] == hashed_my_password:
                print("Login succesful")
    else:
        print("Wrong character please try again.")

#register function
def register():
    new_name = str(input("Name :\t"))
    assert not my_document.document(new_name).get().exists, "This username is already taken, please choose another one."
    new_password = str(input("Password :\t"))
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    new_email = str(input("E-mail :\t"))
    num = str(random.randint(100000, 1000000))
    server.sendmail(sender_email, new_email, num)
    print("Email has been sent to ", new_email)
    code = str(input("Write the code that has been sent to your email adress\t"))
    if code == num:
        my_document.document(new_name).set({
            "email": new_email,
            "password": hashed_password
        })
        print("Register succesful")
    else:
        print("Wrong code, please try again and check if your email is right.")

#change password function
def change_password():
    my_name = str(input("Name :\t"))
    assert my_document.document(my_name).get().exists, "Wrong username, please try again"
    my_email = str(input("E-mail :\t"))
    num = str(random.randint(100000, 1000000))
    server.sendmail(sender_email, my_email, num)
    print("Email has been sent to ", my_email)
    code = str(input("Write the code that has been sent to your email adress"))
    if code == num:
        new_password = str(input("Password :\t"))
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        my_document.document(my_name).set({
        "email": my_email,
        "password": hashed_password
        })
        print("Password changed succesfuly")
    else:
        print("Wrong code, please try again and check if your email is right.")

#main function
def main():
    while True:
        lr = str(input("""Do you have an account?
If yes press l else if press r. :\t"""))
        if lr == "l":
            login()
            break
        elif lr == "r":
            register()
            break
        else:
            print("""You pressed an incorrect character.
Please try again""")

#program starts
main()