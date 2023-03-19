from flask import *
from pyrebase import *

#---------------initializeing application------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')

#---------------configuring firebase----------------------------

firebaseConfig = {'apiKey': "AIzaSyAnxsGxp6e5nqH8L4y5z926N_xD3UEq0W0",
  'authDomain': "eduhive-b888d.firebaseapp.com",
  'projectId': "eduhive-b888d",
  'storageBucket': "eduhive-b888d.appspot.com",
  'messagingSenderId': "949663329841",
  'appId': "1:949663329841:web:6840f25200d1954474ef10",
  'measurementId': "G-ELN6NQQ4TX",
  'databaseURL': ""}

firebase = initialize_app(firebaseConfig)

auth = firebase.auth()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/undergraduate')
def undergraduate():
    return render_template('undergraduate.html')

@app.route('/engineering')
def engineering():
    return render_template('engineering.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/math')
def math():
    return render_template('math.html')

if __name__ == '__main__':
    app.run(debug=True)
    