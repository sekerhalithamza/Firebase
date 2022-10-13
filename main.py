import firebase_admin
from firebase_admin import credentials, firestore
#firebase connection
db = credentials.Certificate("fir-denemler-firebase-adminsdk-5peev-91d25187c4.json")
app = firebase_admin.initialize_app(db)
db = firestore.client()
#creating collection
myDocument = db.collection("users")

def login():
    myName = str(input("Name :\t"))
    myPassword = str(input("Password :\t"))
    try:
        data = myDocument.document(myName).get().to_dict()
        data["password"] 
    except KeyError:
        print('Account not found')
    except AttributeError:
        print("Account not found")
    else: 
        if data["password"] == myPassword:
            print("Giriş başarılı")

def register():
    newName = str(input("Name :\t"))
    assert not db.collection(myDocument).document(newName).get().exists, "There is no such a file"
    newPassword = str(input("Password :\t"))
    myDocument.document(newName).set({
        "password": newPassword
    })

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