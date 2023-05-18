import os # used for getting enviroment variables set during execution
import requests # find an api for getting stock prices, use .env file for hiding the api key

from flask import Flask, render_template, request, jsonify, redirect, make_response
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# make database, maybe use a different db for different data besides username/password
os.environ['DATABASE_URL'] = 'postgresql://localhost/paper-trader'

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/reset')
def resetPassword():
    # function the will direct to html the will reset the user's password
    ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        # make sure account doesn't already exist by username or email
        if db.execute(text("SELECT * FROM users WHERE username = :username"), {'username': username}).rowcount != 0:
            return render_template('register.html', error="Username already in use")
        
        elif db.execute(text("SELECT * FROM users WHERE email = :email"), {'email':email}).rowcount != 0:
            return render_template('register.html', error="Email already in use")

        # make sure email and password are valid
        if username.strip() == "" or email.strip() == "" or password1.strip() == "":
            return render_template('register.html', error="Invalid inputs")
        
        elif password1 != password2:
            return render_template('register.html', error="Passwords do not match")
        
        
            # create rules for what is a valid password
        # login in the user and access the user dashboard
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # access database to see if user is exists and creditials are valid
        # if so login and access the user dashboard
        email = request.form.get('email')
        password = request.form.get('password')

        # get from the db to check
    return render_template('login.html')

@app.route('/dashboard/<string:user>')
def dashboard(user):
    # need to get account balance and account number
    return render_template('dashboard.html', user=user)

@app.route('/<string:user>/<string:name>')
def stockDate(name):
    # this function will be called for getting api requests
    ...

# @app.route()
def buyStock():
    ...

# @app.route()
def sellStock():
    ...

@app.errorhandler(404)
def not_found(parm):
    return make_response(render_template('index.html'), 404)

app.run(debug=True)