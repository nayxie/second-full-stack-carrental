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
        # and request.form.get('userrole') 
        and request.form.get('email')):
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # userRole = request.form['userrole']
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
        elif not username or not password or not email:
            msg = 'Please fill out the form.'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            userRole = 'customer'
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








def checkRole():
    if session['loggedin']:
        if session['userrole'] == 'admin':
            return 'admin'
        elif session['userrole'] == 'staff':
            return 'staff'
        elif session['userrole'] == 'customer':
            return 'customer'
    else:
        return 'None'










@app.route("/adminpage")
def adminPage():
    userrole = checkRole()
    if userrole == 'admin':
        return render_template("adminPage.html")
    elif userrole == 'None':
        redirect(url_for("logIn"))
    else:
        return 'Unauthorised.'

@app.route("/staffpage")
def staffPage():
    userrole = checkRole()
    if userrole == 'staff':
        return render_template("staffPage.html")
    elif userrole == 'None':
        redirect(url_for("logIn"))
    else:
        return 'Unauthorised.'

@app.route("/customerpage")
def customerPage():
    userrole = checkRole()
    if userrole == 'customer':
        return render_template("customerPage.html")
    elif userrole == 'None':
        redirect(url_for("logIn"))
    else:
        return 'Unauthorised.'


# access control need to be implemented from this point 

@app.route("/userform")
def userForm():
    return render_template("userForm.html")

@app.route("/addcustomers", methods=['GET', 'POST'])
def addCustomers():
    msg = ""
    if (request.method == 'POST' 
        and request.form.get('username') 
        and request.form.get('password') 
        and request.form.get('firstname') 
        and request.form.get('lastname') 
        and request.form.get('address') 
        and request.form.get('email')
        and request.form.get('phone')):
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers.'
        elif not re.match(r'^[A-Za-z\s]+$', firstname):
            msg = 'Invalid first name.'
        elif not re.match(r'^[A-Za-z\s]+$', lastname):
            msg = 'Invalid last name.'
        elif not re.match(r'^[A-Za-z0-9\s\-,.#]+$', address):
            msg = 'Invalid address.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not re.match(r'^[\d\s+\-().]+$', phone):
            msg = 'Invalid phone number.'
        # elif not username or not password or not userRole or not email:
        #     msg = 'Please fill out the form.'
        else:
            userrole = "customer"
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # print(hashed)
            cursor.execute('INSERT INTO users (Username, UserPassword, UserRole, FirstName, LastName, Address, Email, Phone) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (username, hashed, userrole, firstname, lastname, address, email, phone,))
            mysql.connection.commit()
            msg = 'You have successfully added a customer!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    return msg

@app.route("/customerlist")
def customerList():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE UserRole = "customer"')
    account = cursor.fetchall()
    return render_template("customerList.html", account=account)

@app.route("/customerinfo/<username>")
def customerInfo(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
    account = cursor.fetchone()
    return render_template("displayInfo.html", account=account)

@app.route("/updateinfo", methods=['GET', 'POST'])
def updateInfo():
    msg = ""
    if (request.method == 'POST' 
        and request.form.get('username') 
        # and request.form.get('password') 
        and request.form.get('firstname') 
        and request.form.get('lastname') 
        and request.form.get('address') 
        and request.form.get('email')
        and request.form.get('phone')):

        username = request.form['username']
        # password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
    
        if not re.match(r'^[A-Za-z\s]+$', firstname):
            msg = 'Invalid first name.'
        elif not re.match(r'^[A-Za-z\s]+$', lastname):
            msg = 'Invalid last name.'
        elif not re.match(r'^[A-Za-z0-9\s\-,.#]+$', address):
            msg = 'Invalid address.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not re.match(r'^[\d\s+\-().]+$', phone):
            msg = 'Invalid phone number.'
        # elif not username or not password or not userRole or not email:
        #     msg = 'Please fill out the form.'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE users SET FirstName = %s, LastName= %s, Address= %s, Email= %s, Phone= %s WHERE Username = %s;',
                            (firstname, lastname, address, email, phone, username))
            mysql.connection.commit()
            msg = 'You have successfully updated a customer!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    return msg

@app.route("/customerlist2")
def customerList2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE UserRole = "customer"')
    account = cursor.fetchall()
    return render_template("customerList2.html", account=account)

@app.route("/deletecustomers/<username>")
def deleteCustomers(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM users WHERE Username = %s', (username,))
    mysql.connection.commit()
    msg = 'You have successfully deleted a customer!'
    return msg












