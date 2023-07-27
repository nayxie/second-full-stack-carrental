from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
import mysql.connector
from mysql.connector import FieldType
import connect

from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt


   


app = Flask(__name__)

# My secret key for extra protection)
app.secret_key = 'ABC123'

# Database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'rentalcars'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)




@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def logIn():
    return render_template("logIn.html")

@app.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
    username = request.form['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
    account = cursor.fetchone()
    print(account)
    return "going through ok"

    # msg = ''
    # # Check if "username" and "password" POST requests exist (user submitted form)
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     # Create variables for easy access
    #     username = request.form['username']
    #     userPassword = request.form['password']
    #     # Check if account exists using MySQL
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
    #     # Fetch one record and return result
    #     account = cursor.fetchone()
    #     if account is not None:
    #         password = account['UserPassword']
    #         if bcrypt.checkpw(userPassword.encode('utf-8'),password.encode('utf-8')):
    #         # If account exists in accounts table in out database
    #         # Create session data, we can access this data in other routes
    #             session['loggedin'] = True
    #             session['id'] = account['UserID']
    #             session['username'] = account['Username']
    #             # Redirect to home page
    #             return redirect(url_for('home'))
    #         else:
    #             #password incorrect
    #             msg = 'Incorrect password!'
    #     else:
    #         # Account doesnt exist or username incorrect
    #         msg = 'Incorrect username'
    # # Show the login form with message (if any)
    # return msg


# route and function here to deal with log in information
# fetch username and password 
# if usermname doesn't exist, or username and pw don't match, display msg
# if correct, display a message "welcome {firstname lastname}! role: {role}"
# display links accordingly 




# hashing password:
# hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
