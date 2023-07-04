from functions import validEmail, validPass
from SystemAPI.stocksV2 import StockAPI
from database.database import Database

import os
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

database = Database()

stockAPI = StockAPI()

@app.route("/")
def index():
    session.clear()
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
        
        elif not validPass(password1) or not validEmail(email):
            return render_template('register.html', error="Invalid inputs")
        
        elif password1 != password2:
            return render_template('register.html', error="Passwords do not match")

        result = database.register(db, email, username, password1)

        if not result[0]:
            return render_template('register.html', error=result[1])

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

        #result = db.execute(text("SELECT username FROM users WHERE email = :email AND pass = :pass"), {'email': email, 'pass':password})
        
        # if result.rowcount != 0:
        if user:=database.login(db, email, password):
            session['username'] = user

            if user == 'admin':
                return redirect('/admin')

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
    balance = database.getBalance(db, user)
    

    stocks = database.getStocks(db, user)

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
    
    stocks = database.getStocks(db, user)

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
    return make_response(render_template('search.html', user=user, stocks=stocks), 200)

@app.route('/logout')
def logout():
    session.pop('username', None)

    return redirect('/')

@app.errorhandler(404)
def not_found(parm):
    return make_response(render_template('index.html'), 404)

@app.errorhandler(500)
def broke(parm):
    session.clear()
    return make_response(render_template('index.html'), 500)


# admin functions==================================================

@app.route('/admin')
def admin_page():
    if session.get('username') != 'admin':
        return redirect('/')
    
    # get all users and return a dashboard
        # set up html template
        # designate its own js file

    users = database.getAllUsers(db)
    balance = database.getAllBalances(db)

    return render_template('admin.html', users=users, balance=balance)

    

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
    amount = float(data['amount'])

    # check if valid operation
    # balance = list(map(lambda x: x[0],db.execute(text("SELECT balance FROM balances WHERE username = :username"), {'username': username}).fetchall()))[0]
    balance = database.getBalance(db, username)

    if amount > balance or amount == 0:
        return 

    res = stockAPI.buy_stock(stock, amount)

    shares = res[0]
    sharePrice = res[1]

    # db handling
    # check if some is already owned
    # result = db.execute(text('SELECT * FROM purchases WHERE username = :username AND syml = :syml'), {'username': username, 'syml': stock})
    
    result = database.getStock(db, username, stock)
    # if result.rowcount != 0:
    if result:
        # if so, update
        # result = result.fetchall()[2]
        result = result[2]

        newValue = result + shares

        # db.execute(text('UPDATE purchases SET shares = :shares WHERE username = :username AND syml = :syml'), {'shares':newValue, 'username': username, 'syml': stock})
        # db.commit()

        database.updateStock(db, username, stock, newValue)

    # else add
    else:
        # db.execute(text('INSERT INTO purchases (username, shares, syml) VALUES (:username, :shares, syml)'), {'username': username, 'shares': shares, 'syml': stock})
        # db.commit
        database.addStock(db, username, stock, shares)
    
    # update balance
    # db.execute(text('UPDATE balances SET balances = :balance WHERE username = :username'), {'balance': (balance - amount), 'username': username})
    # db.commit()
    database.updateBalance(db, (balance - amount), username)

    emit('returnBuy', {'shares':shares, 'sharePrice':sharePrice})


@socketio.on('sell')
def sellStock(data):
    if not (username:=session.get('username')):
        return None
    
    stock = data['stock']
    shares = float(data['shares'])
    
    # check if valid operation
    try:
        stockCount = (list(map(lambda x: x[0], db.execute(text('SELECT shares FROM purchases WHERE username = :username AND syml = :syml'), {'username':username, 'syml': stock}).fetchall()))[0])
    except:
        return

    if shares > stockCount or shares == 0:
        return

    res = stockAPI.sell_stock(stock, shares)

    amount = res[0]
    sharePrice = res[1]

    # db handling
    remaining = float(stockCount) - shares

    if not remaining:
        # delete from db
        db.execute(text('DELETE FROM purchases WHERE username = :username AND syml = :syml'), {'username':username, 'syml':stock})
        db.commit()
    else:
        # update in db
        db.execute(text('UPDATE purchases SET shares = :shares WHERE username = :username AND syml = :syml'), {'shares': remaining, 'username': username, 'syml': stock})
        db.commit()

    # edit balance
    balance = float(list(map(lambda x: x[0], db.execute(text('SELECT balance FROM balances WHERE username = :username'), {'username': username}).fetchall()))[0]) + amount

    db.execute(text('UPDATE balances SET balance = :balance WHERE username = :username'), {'balance': balance, 'username':username})
    db.commit()

    emit('returnSell', {'amount': amount, 'sharePrice':sharePrice})

@socketio.on('hello')
def hello(data):
    stock = data['symbol']
    price = stockAPI.getPrice(stock)

    return {'price':price}

@socketio.on('delete')
def deleteUser(data):
    user = data.get('user', None)
    email = data.get('email', None)

    if user is None or email is None or session.get('username') != 'admin':
        return False

    res = database.deleteUser(db, user, email)

    return res


app.run(debug=True, threaded=True)
