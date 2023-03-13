from flask import *

app = Flask(__name__, template_folder='templates', static_folder='static')


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

if __name__ == '__main__':
    app.run(debug=True)
    