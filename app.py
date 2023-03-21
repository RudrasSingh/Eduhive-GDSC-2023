from flask import *
from pyrebase import *
import requests

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

#-------------------------security key (do not change/remove this code)---------------------------------------

app.secret_key = "SECRET_KEY"
#-----------------------page routes-----------------------------------------


@app.route('/')
def home():
    
    if 'user' in session:

        #signed user
        
        user_id_token = session['user']["idToken"]
        auth.refresh(session['user']['refreshToken'])


        user = auth.get_account_info(user_id_token)['users'][0]
        first_name = ""
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]
        return render_template('index.html', first_name=first_name)
    
    else:
        #unsigned user
        return render_template('index.html')




@app.route('/signup', methods = ['GET','POST'])

def signup():

    if request.method == 'POST':

        newname = request.form['newname']
        newemail = request.form['newemail']
        newpassword = request.form['newpassword']


        try:
            
            user = auth.create_user_with_email_and_password(newemail, newpassword)

            auth.update_profile(user["idToken"], display_name = newname)

            

            return redirect('/login')

            
        except Exception as e:
            
            message = json.loads(e.args[1])['error']['message']
            
            if message == "EMAIL_EXISTS":

                
                return render_template('login.html', signup_error = "Email already exists. Login with you registered email or register with a new one.", signup_display_error = True)
            
            
            else:

                return render_template('login.html', signup_error = "Something is not right. Please try again later or contact the administrator", signup_display_error = True)

            

    
    else:


        signup_error_message = "Something is not right. Please try again later or contact the administrator"
        return render_template('login.html', signup_error = signup_error_message, signup_display_error = True)


@app.route('/login', methods = ['GET','POST'])
def login():
    
    login_display_error = False
    print("login execution")

    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        
        try:
            
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect('/')
        
        except Exception as e:
        
            login_error = "Invalid email or password. Please try again."
            return render_template('login.html', login_error = login_error, login_display_error = True)
        
    else:
        return render_template('login.html')




@app.route('/logout')
def logout():



    session.pop('user', None)
    session.clear() 


    return redirect('/')




@app.route('/dashboard')

def dashboard():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = ""
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('dashboard.html', first_name=first_name)


    else:

        return redirect('/login')


@app.route('/undergraduate')
def undergraduate():
    return render_template('undergraduate.html')



@app.route('/engineering')
def engineering():
    return render_template('engineering.html')





@app.route('/math')
def math():
    return render_template('math.html')

if __name__ == '__main__':
    app.run(debug=True)
    