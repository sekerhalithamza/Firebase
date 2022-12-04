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
db = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(db)
db = firestore.client()

#creating a collection in firebase firestore database
user_document = db.collection("users")
admin_document = db.collection("admin")

#logging into email
sender_email = "halitsbot"
email_password = "rbflhssxgdwsbgkg"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, email_password)

#login function
def login():
    my_name = str(input("Name :\t"))
    assert user_document.document(my_name).get().exists, "Wrong username, please try again."
    my_password = str(input("Password :\t"))
    hashed_my_password = hashlib.sha256(my_password.encode()).hexdigest()
    try:
        data = user_document.document(my_name).get().to_dict()
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
    assert not user_document.document(new_name).get().exists, "This username is already taken, please choose another one."
    new_password = str(input("Password :\t"))
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    new_email = str(input("E-mail :\t"))
    num = str(random.randint(100000, 1000000))
    server.sendmail(sender_email, new_email, num)
    print("Email has been sent to ", new_email)
    code = str(input("Write the code that has been sent to your email adress\t"))
    if code == num:
        user_document.document(new_name).set({
            "email": new_email,
            "password": hashed_password
        })
        print("Register succesful")
    else:
        print("Wrong code, please try again and check if your email is right.")

#change password function
def change_password():
    my_name = str(input("Name :\t"))
    assert user_document.document(my_name).get().exists, "Wrong username, please try again"
    my_email = str(input("E-mail :\t"))
    try:
        data = user_document.document(my_name).get().to_dict()
        data["email"]
    except KeyError:
        print("Email not found")
    except AttributeError:
        print("Email not found")
    else:
        if data["email"] == my_email:
            num = str(random.randint(100000, 1000000))
            server.sendmail(sender_email, my_email, num)
            print("Email has been sent to ", my_email)
            code = str(input("Write the code that has been sent to your email adress"))
            if code == num:
                new_password = str(input("Password :\t"))
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                user_document.document(my_name).set({
                    "email": my_email,
                    "password": hashed_password
                })
                print("Password changed succesfuly")
            else:
                print("Wrong code, please try again and check if your email is right.")
        else:
            print("Wrong Email")

###############################################################################################################################################
###################################################### ADMIN PART #############################################################################
###############################################################################################################################################

#admin console function
def admin_login():
    my_name = str(input("Name :\t"))
    assert admin_document.document(my_name).get().exists, "Wrong username, please try again"
    my_email = str(input("E-mail :\t"))
    try:
        data = admin_document.document(my_name).get().to_dict()
    except KeyError:
        print("Email not found")
    except AttributeError:
        print("Email not found")
    else:
        my_password = str(input("Pasword :\t"))
        hashed_password = hashlib.sha256(my_password.encode()).hexdigest()
        if data["password"] == hashed_password:
            if data["email"] == my_email:
                num = str(random.randint(100000, 1000000))
                server.sendmail(sender_email, my_email, num)
                print("Email has been sent to ", my_email)
                code = str(input("Write the code that has been sent to your email adress"))
                if code == num:
                    print("Login succesful")
                    admin_console()
                else:
                    print("Wrong code, please try again and check if your email is right.")
            else:
                print("Wrong email")
        else:
            print("Wrong password")

#adding a new admin to firebase database function
def add_admin():
    new_name = str(input("Name :\t"))
    assert not admin_document.document(new_name).get().exists, "This username is already taken, please choose another one."
    new_password = str(input("Password :\t"))
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    new_email = str(input("E-mail :\t"))
    num = str(random.randint(100000, 1000000))
    server.sendmail(sender_email, new_email, num)
    print("Email has been sent to ", new_email)
    code = str(input("Write the code that has been sent to your email adress\t"))
    if code == num:
        admin_document.document(new_name).set({
            "email": new_email,
            "password": hashed_password
        })
        print("Register succesful")
    else:
        print("Wrong code, please try again and check if your email is right.")

#
def add_user():
    new_name = str(input("Name :\t"))
    assert not user_document.document(new_name).get().exists, "This username is already taken, please choose another one."
    new_password = str(input("Password :\t"))
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    new_email = str(input("E-mail :\t"))
    num = str(random.randint(100000, 1000000))
    server.sendmail(sender_email, new_email, num)
    print("Email has been sent to ", new_email)
    code = str(input("Write the code that has been sent to your email adress\t"))
    if code == num:
        user_document.document(new_name).set({
            "email": new_email,
            "password": hashed_password
        })
        print("Register succesful")
    else:
        print("Wrong code, please try again and check if your email is right.")

#
def delete_user():
    my_name = str(input("Name :\t"))
    assert user_document.document(my_name).get().exists, "There is not such an user name, please try again"
    user_document.document(my_name).delete()
    print("User deleted succesfuly")

#deletin an admin from firebase database function
def delete_admin():
    my_name = str(input("Name :\t"))
    assert admin_document.document(my_name).get().exists, "There is not such an admin name, please try again"
    admin_document.document(my_name).delete()
    print("Admin deleted succesfuly")


#admin console function
def admin_console():
    while True:
        print("""
To add new admin press 1,

To delete an admin press 2,

To change an admins password or email press 3,

To add a new user press 4,

To delete an user press 5,

To change an users password or email press 6,

To log out press 7.
""")
#TODO: Complete the admin console
        admin_string = str(input(""))
        match admin_string:
            case "1":
                print("Directing...")
                add_admin()
            case "2":
                print("Directing...")
                delete_admin()
            case "3":
                print("Directing...")
            case "4":
                print("Directing...")
                add_user()
            case "5":
                print("Directing...")
                delete_user()
            case "6":
                print("Directing...")
            case "7":
                print("Logging out")
                break

#main function
def main():
    while True:
        print("""
To login press l or L,

To register press r or R,

To change password press c or C.

To log out press b or B.
""")
        user_string = str(input("")).upper()
        match user_string:
            case "L":
                login()
            case "R":
                register()
            case "C":
                change_password()
            case "120607":
                print("You reached to admin panel.")
                print("Please log in.")
                admin_login()
                break
            case "B":
                print("Logging out")
                break

#program starts
if __name__ == "__main__":
    main()

#TODO: Add a online/offline statu