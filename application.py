from functions import validEmail, validPass
from SystemAPI.stocksV2 import StockAPI

import os # used for getting enviroment variables set during execution
import requests # find an api for getting stock prices, use .env file for hiding the api key
from dotenv.main import load_dotenv

from flask import Flask, render_template, request, jsonify, redirect, make_response, session
from flask_session import Session
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

load_dotenv()
DBuser = os.getenv('DBuser')
DBpassword = os.getenv('DBpassword')

if DBuser is None or DBpassword is None:
    raise KeyError

# make database, maybe use a different db for different data besides username/password
os.environ['DATABASE_URL'] = f'postgresql://{DBuser}:{DBpassword}@localhost/paper-trader'

if not os.getenv('DATABASE_URL'):
    raise RuntimeError("DATABASE_URL is not set")

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


stockAPI = StockAPI()

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
        # create rules for what is a valid password

        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # make sure that inputs are valid
        if username.strip() == "" or email.strip() == "" or password1.strip() == "":
            return render_template('register.html', error="Invalid inputs")
        
        elif not validPass(password1):
            return render_template('register.html', error="Password is not valid")
        
        elif not validEmail(email):
            return render_template('register.html', error="Invalid email")
        
        elif password1 != password2:
            return render_template('register.html', error="Passwords do not match")
        

        # make sure account doesn't already exist by username or email
        if db.execute(text("SELECT * FROM users WHERE username = :username"), {'username': username}).rowcount != 0:
            return render_template('register.html', error="Username already in use")
        
        elif db.execute(text("SELECT * FROM users WHERE email = :email"), {'email':email}).rowcount != 0:
            return render_template('register.html', error="Email already in use")

        # creates account and balance and assigns session variable
        db.execute(text('INSERT INTO users (username, email, pass) VALUES (:username, :email, :password)'), {'username': username, 'email':email, 'password': password1})
        db.execute(text('INSERT INTO balances (username, balance) VALUES (:username, :balance)'), {'username': username, 'balance': 0})
        db.commit()

        session['username'] = username

        return redirect(f'/dashboard/{username}')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # access database to see if user is exists and creditials are valid
        # if so login and access the user dashboard
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.execute(text("SELECT username FROM users WHERE email = :email AND pass = :pass"), {'email': email, 'pass':password})

        if result.rowcount != 0:
            # get username and load the dashboard and make the session token
            result = result.fetchone()

            user = result[0]
            session['username'] = user

            return redirect(f'/dashboard/{user}')

        # get from the db to check
    return render_template('login.html')

@app.route('/dashboard/<string:user>')
def dashboard(user):
    # check to make sure the user is logged in when requested
    if not (username := session.get('username')):
        return redirect('/')

    if username != user:
        return redirect('/')
    
    # need to get account balance and account number
    balance = db.execute(text('SELECT balance from balances WHERE username = :username'), {'username':user}).fetchone()[0]
    
    stocks = db.execute(text('SELECT syml, shares from purchases WHERE username = :username'), {'username': user}).fetchall()

    stocks = list(map(lambda x: [x[0], float(x[1])], stocks))

    value = 0

    for pair in stocks:
        completed = False
        
        while not completed:
            try:
                pair.append(stockAPI.getPrice(pair[0]) * pair[1])
                value += pair[2]
                completed = True
            except:
                continue
    
    value = round(value, 2)

    return render_template('dashboard.html', user=user, balance=balance, stocks=stocks, value=value)

@app.route('/manage/<string:user>')
def manage(user):
    if not (username:=session.get('username')):
        return redirect('/')

    if username != user:
        return redirect('/')
    
    stocks = list(map(lambda x: [x[0], float(x[1])], db.execute(text('SELECT syml, shares from purchases WHERE username = :username'), {'username':user}).fetchall()))
    
    return render_template('manage.html', user=user, stocks=stocks)

@app.route('/settings/<string:user>')
def settings(user):
    if not (username:=session.get('username')):
        return redirect('/')

    if username != user:
        return redirect('/')
    
    return render_template('settings.html', user=user)

@app.route('/search/<string:user>', methods=['GET', 'POST'])
def search(user):
    if not (username:=session.get('username')):
        return redirect('/')
    
    if username != user:
        return redirect('/')
    
    stocks = []
    if request.method == 'POST':
        if request.form.get('search').strip() != '':
            # seaching part of method, assign search results into stocks list
            ...
    return render_template('search.html', user=user, stocks=stocks)

@app.route('/logout')
def logout():
    session.pop('username', None)

    return redirect('/')

@app.errorhandler(404)
def not_found(parm):
    return make_response(render_template('index.html'), 404)



# socket functions=================================================


@socketio.on('price')
def getPrice(data):
    stock = data['stock']
    method = data['method']
    
    value = stockAPI.getPrice(stock)

    emit('priceReturn', {'value': value, 'stock': stock, 'method': method})

@socketio.on('buy')
def buyStock(data):
    if not (username:=session.get('username')):
        return None
    
    stock = data['stock']
    amount = data['amount']

    # check if valid operation
    balance = list(map(lambda x: x[0],db.execute(text("SELECT balance FROM balances WHERE username = :username"), {'username': username}).fetchall()))[0]

    if amount > balance or amount == 0:
        return 

    res = stockAPI.buy_stock(stock, amount)

    shares = res[0]
    sharePrice = res[1]

    # db handling
    # check if some is already owned
    result = db.execute(text('SELECT * FROM purchases WHERE username = :username AND syml = :syml'), {'username': username, 'syml': stock})
    if result.rowcount != 0:
        # if so, update
        result = result.fetchall()[2]

        newValue = result + shares

        db.execute(text('UPDATE purchases SET shares = :shares WHERE username = :username AND syml = :syml'), {'shares':newValue, 'username': username, 'syml': stock})
        db.commit()

    # else add
    else:
        db.execute(text('INSERT INTO purchases (username, shares, syml) VALUES (:username, :shares, syml)'), {'username': username, 'shares': shares, 'syml': stock})
        db.commit
    
    # update balance
    db.execute(text('UPDATE balances SET balances = :balance WHERE username = :username'), {'balance': (balance - amount), 'username': username})
    db.commit()

    emit('returnBuy', {'shares':shares, 'sharePrice':sharePrice})


@socketio.on('sell')
def sellStock(data):
    if not (username:=session.get('username')):
        return None
    
    stock = data['stock']
    shares = data['shares']
    
    # check if valid operation
    stockCount = list(map(lambda x: x[0], db.execute(text('SELECT shares FROM purchases WHERE username = :username AND syml = :syml'), {'username':username, 'syml': stock}).fetchall()))

    if shares > stockCount or shares == 0:
        return

    res = stockAPI.sell_stock(stock, shares)

    amount = res[0]
    sharePrice = res[1]

    # db handling
    remaining = stockCount - shares

    if not remaining:
        # delete from db
        db.execute(text('DELETE FROM purchases WHERE username = :username AND syml = :syml'), {'username':username, 'syml':stock})
        db.commit()
    else:
        # update in db
        db.execute(text('UPDATE purchases SET shares = :shares WHERE username = :username AND syml = :syml'), {'shares': remaining, 'username': username, 'syml': stock})
        db.commit()

    # edit balance
    balance = list(map(lambda x: x[0], db.execute(text('SELECT balance FROM balances WHERE username = :username'), {'username': username}).fetchone()))[0] + amount

    db.execute(text('UPDATE balances SET balance = :balance WHERE username = :username'), {'balance': balance, 'username':username})
    db.commit()

    emit('returnSell', {'amount': amount, 'sharePrice':sharePrice})

app.run(debug=True, threaded=True)