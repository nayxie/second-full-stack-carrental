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

# My secret key for extra protection
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
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        # Create variables for easy access
        username = request.form['username']
        userPassword = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account['UserPassword']
            if bcrypt.checkpw(userPassword.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['UserID']
                session['username'] = account['Username']
                session['userrole'] = account['UserRole']
                # Redirect to dashboard based on user role
                if session['userrole'] == 'admin':
                    return redirect(url_for('adminPage'))
                elif session['userrole'] == 'staff':
                    return redirect(url_for('staffPage'))
                elif session['userrole'] == 'customer':
                    return redirect(url_for('customerPage'))






            else:
                #password incorrect
                msg = 'Incorrect password.'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username.'
    else:
        msg = 'Please provide both username and password.'
    # Show the login form with message
    return msg

@app.route("/signup")
def signUp():
    return render_template("signUp.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    # Check if "username", "password" "userrole" "email" POST requests exist (user submitted form)
    if (request.method == 'POST' 
        and request.form.get('username') 
        and request.form.get('password') 
        and request.form.get('userrole') 
        and request.form.get('email')):
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        userRole = request.form['userrole']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers.'
        elif not username or not password or not userRole or not email:
            msg = 'Please fill out the form.'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # print(hashed)
            cursor.execute('INSERT INTO users (Username, UserPassword, UserRole, Email) \
                            VALUES (%s, %s, %s, %s)', (username, hashed, userRole, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            


            # redirect to login page





    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    # Show registration form with message (if any)
    return msg

@app.route("/adminpage")
def adminPage():
    return render_template("adminPage.html")

@app.route("/staffpage")
def staffPage():
    return render_template("staffPage.html")

@app.route("/customerpage")
def customerPage():
    return render_template("customerPage.html")











# hashing password:
# hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
