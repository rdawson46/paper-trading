import os
import requests

from flask import Flask, render_template, request, jsonify, redirect, make_response
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# os.environ['DATABASE_URL'] = 'postgresql://localhost/

# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # make sure account doesn't already exist
        # make sure email and password are valid
            # create rules for what is a valid password
        # login in the user and access the user dashboard
        ...
    return render_template('register.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # access database to see if user is exists and creditials are valid
        # if so login and access the user dashboard
        ...
    return render_template('login.html')

@app.route('/dashboard/<string:user>')
def dashboard(user):
    return render_template('dashboard.html', user=user)

@app.errorhandler(404)
def not_found(parm):
    return make_response(render_template('index.html'), 404)

app.run(debug=True)