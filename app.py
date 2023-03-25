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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            message = "Success! Password reset link has been sent to your email"
            return render_template('login.html', message=message, display_alert=True)
        except Exception as e:
            message = json.loads(e.args[1])['error']['message']
            
            if message == "EMAIL_NOT_FOUND":


                return render_template('forgot_password.html', message = "Email does not exists. Enter your registered email id!", display_error = True)
            
            
            else:

                return render_template('forgot_password.html', message = "Something is not right. Please try again later or contact the administrator", display_error = True)
    else:
        return render_template('forgot_password.html')




'''# define the route for reset password page
@app.route('/reset_password/<oobCode>', methods=['GET', 'POST'])
def reset_password(oobCode):
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            message = ('error', 'Passwords do not match.')
            return render_template('reset_password.html', message=message, oobCode=oobCode)
        try:
            auth.confirm_password_reset(oobCode, password)
            message = ('success', 'Password reset successfully.')
            return render_template('reset_password.html', message=message, oobCode=oobCode)
        except Exception as e:
            message = ('error', str(e))
            return render_template('reset_password.html', message=message, oobCode=oobCode)
    else:
        return render_template('reset_password.html', oobCode=oobCode)



# define the route for regenerating the password reset link
@app.route('/regenerate_reset_link/<oobCode>', methods=['POST'])
def regenerate_reset_link(oobCode):
    try:
        auth.send_password_reset_email(auth.get_oob_confirmation_code(oobCode)['email'])
        return 'Password reset link has been regenerated. Check your email.'
    except Exception as e:
        return str(e)'''




@app.route('/google-login')
def google_login():
    auth_url = auth.build_auth_url({'providerId': 'google.com'}, {'redirect_uri': url_for('google_auth', _external=True)})
    return redirect(auth_url['authUri'])

@app.route('/google-auth')
def google_auth():
    # Get the authorization code from the query parameters.
    authorization_code = request.args.get('code')

    # Exchange the authorization code for an access token and ID token.
    try:
        credentials = auth.build_credentials_from_google(authorization_code)
        access_token = credentials.get('access_token')
        id_token = credentials.get('id_token')
    except:
        return "Failed to exchange authorization code for access token and ID token"

    # Sign in or create a user using the Google access token and ID token.
    try:
        user = auth.sign_in_with_oauth_token({'google': access_token})
    except:
        email = request.args.get('email')
        password = 'password' # Generate a random password for the user.
        user = auth.create_user_with_email_and_password(email, password)
        auth.update_user(user['idToken'], {'providers': ['google.com']})
        auth.sign_in_with_oauth_token({'google': access_token})

    # Store the user's Firebase ID token in the session.
    session['id_token'] = user['idToken']

    return redirect(url_for('home'))



@app.route('/undergraduate')
def undergraduate():
    
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

        return render_template('undergraduate.html', first_name=first_name)


    else:
        return render_template('undergraduate.html')



@app.route('/engineering')
def engineering():
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

        return render_template('engineering.html', first_name=first_name)


    else:

        return redirect('engineering.html')


 


@app.route('/math')
def math():
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

        return render_template('math.html', first_name=first_name)


    else:

        return redirect('math.html')

if __name__ == '__main__':
    app.run(debug=True)
    