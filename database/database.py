from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.sql import text
from typing import Union

from cryptography.fernet import Fernet
from dotenv.main import load_dotenv
import os
from random import randint as salt

class Database:
    def __init__(self):
        load_dotenv(dotenv_path='./../env')

        db_key = os.getenv('FERNETKEY')
        self.cipher = Fernet(db_key)

    def getAllUsers(self, db: scoped_session[Session]):
        """
        return all values from the users table
        """
        return db.execute(text('Select * from users WHERE username != \'admin\'')).fetchall()



    def getAllBalances(self, db:scoped_session[Session]):
        """
        returns all values from the balances table
        """
        return db.execute(text('SELECT * FROM balances WHERE username != \'admin\'')).fetchall()



    def getUser(self, db: scoped_session[Session], username):
        """
        returns a singular user from their username
        """
        return db.execute(text("SELECT * FROM users WHERE username = :username"), {'username': username}).fetchone()
    


    def login(self, db:scoped_session[Session], email, password) -> Union[str, None]:
        """
        will return a value if user exists, none if else
        """
        
        if (result:=db.execute(text('SELECT * FROM users WHERE email = :email'), {'email':email})).rowcount == 0:
            return None
        
        result = result.fetchone()
        
        decoded = self.cipher.decrypt(bytes(result[2], 'utf-8')).decode('utf-8')

        if decoded != password:
            return None

        return result[0]
    


    def register(self, db:scoped_session[Session], email, username, password)->Union[bool, str]:
        """
        will handle user creation is users and balances table
        [success, error]
        """
        emailResult = db.execute(text("SELECT * FROM users WHERE email = :email"), {'email':email})
        usernameResult = db.execute(text("SELECT * FROM users WHERE username = :username"), {'username': username})

        if emailResult.rowcount > 0:
            return [False, "Email already in use"]
        elif usernameResult.rowcount > 0:
            return [False, "Username already in use"]
        
        password = self.cipher.encrypt(bytes(password, encoding='utf-8')).decode('utf-8')
        
        db.execute(text('INSERT INTO users (username, email, pass) VALUES (:username, :email, :password)'), {'username': username, 'email':email, 'password': password})
        db.execute(text('INSERT INTO balances (username, balance) VALUES (:username, :balance)'), {'username': username, 'balance': 0})
        db.commit()

        return [True, '']
    


    def deleteUser(self, db:scoped_session[Session], username, email):
        try:
            db.execute(text('DELETE FROM users WHERE username = :username and email = :email'), {'username':username, 'email':email})
            db.execute(text('DELETE FROM balances WHERE username = :username'), {'username':username})
            db.execute(text('DELETE FROM purchases WHERE username = :username'), {'username':username})
            db.commit()
            return True
        except:
            return False


    def getBalance(self, db:scoped_session[Session], username):
        """
        returns the values of balances for a singular user
        """
        return db.execute(text('SELECT balance from balances WHERE username = :username'), {'username':username}).fetchone()[0]
    


    def updateBalance(self, db:scoped_session[Session], balance, username):
        """
        update balance amount for a user
        """
        db.execute(text('UPDATE balances SET balance = :balance WHERE username = :username'), {'balance': balance, 'username': username})
        db.commit()
        return True

    

    def getStocks(self, db:scoped_session[Session], username) -> list:
        """
        returns all stocks for one user and formats for use
        """
        return list(map(lambda x: [x[0], float(x[1])], db.execute(text('SELECT syml, shares from purchases WHERE username = :username'), {'username':username}).fetchall()))
    


    def getStock(self, db:scoped_session[Session], username, syml):
        """
        returns the data about one stock for one user
        """
        return db.execute(text('SELECT * FROM purchases WHERE username = :username AND syml = :syml'), {'username':username, 'syml':syml}).fetchone()
    


    def updateStock(self, db:scoped_session[Session], username, syml, newValue):
        try:
            db.execute(text('UPDATE purchases SET shares = :shares WHERE username = :username AND syml = :syml'), {'shares':newValue, 'username': username, 'syml': syml})
            db.commit()
            return True
        except:
            return False
    


    def addStock(self, db:scoped_session[Session], username, syml, shares):
        db.execute(text('INSERT INTO purchases (username, shares, syml) VALUES (:username, :shares, :syml)'), {'username': username, 'shares': shares, 'syml': syml})
        db.commit
        return True