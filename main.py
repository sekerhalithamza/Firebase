import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

#firebase connection
db = credentials.Certificate("./sign-up-sign-in-python-firebase-adminsdk-8kbfq-e0afe42a03.json")
app = firebase_admin.initialize_app(db)
db = firestore.client()

#creating collection
my_document = db.collection("users")

#login function
def login():
    my_name = str(input("Name :\t"))
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
            print("Giriş başarılı")

#register function
def register():
    new_name = str(input("Name :\t"))
    assert not my_document.document(new_name).get().exists, "There is no such a file"
    new_password = str(input("Password :\t"))
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    my_document.document(new_name).set({
        "password": hashed_password
    })

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
         
main()