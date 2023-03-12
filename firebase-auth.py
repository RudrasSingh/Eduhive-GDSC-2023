import pyrebase  


firebaseConfig = {'apiKey': "AIzaSyAnxsGxp6e5nqH8L4y5z926N_xD3UEq0W0",
  'authDomain': "eduhive-b888d.firebaseapp.com",
  'projectId': "eduhive-b888d",
  'storageBucket': "eduhive-b888d.appspot.com",
  'messagingSenderId': "949663329841",
  'appId': "1:949663329841:web:6840f25200d1954474ef10",
  'measurementId': "G-ELN6NQQ4TX",
  'databaseURL': ""}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

def signup():
    email =  input("Enter Email - ")
    password = input("Enter Password - ")
    try:
        user =  auth.create_user_with_email_and_password(email,password)
        print("Successfully created an account!")
    except Exception as e:
        print(e," Email Already exists!") 
 

def login():
    print("Log in....")
    pass


