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

def isAuthenticated():
    return 'username' in session

def getUserRole():
    if isAuthenticated():
        if session['userrole'] == 'admin':
            return 'admin'
        elif session['userrole'] == 'staff':
            return 'staff'
        elif session['userrole'] == 'customer':
            return 'customer'
    return None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def logIn():
    return render_template("logIn.html")

@app.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
    msg = ''
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
                # session['loggedin'] = True
                session['id'] = account['UserID']
                session['username'] = account['Username']
                session['userrole'] = account['UserRole']
                # Redirect to dashboard based on user role
                return redirect(url_for('dashboard'))
            
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

@app.route("/dashboard")
def dashboard():
    if not isAuthenticated():
        return redirect(url_for('home'))
    if session['userrole'] == 'admin':
        return render_template('adminPage.html')
    elif session['userrole'] == 'staff':
        return render_template('staffPage.html')
    elif session['userrole'] == 'customer':
        return render_template('customerPage.html')
    return redirect(url_for("home"))

@app.route("/logout")
def logOut():
    session.clear()
    return redirect(url_for("home"))

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
            return 'Account already exists.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return 'Invalid email address.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            return 'Username must contain only characters and numbers.'
        elif not username or not password or not email:
            return 'Please fill out the form.'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            userRole = 'customer'
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # print(hashed)
            cursor.execute('INSERT INTO users (Username, UserPassword, UserRole, Email) \
                            VALUES (%s, %s, %s, %s)', (username, hashed, userRole, email,))
            mysql.connection.commit()
            return 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        return 'Please fill out the form.'
    # Show registration form with message (if any)
    return redirect(url_for("signUp"))



# @app.route("/adminpage")
# def adminPage():
#     if not isAuthenticated():
#         return redirect(url_for('home'))
#     userrole = getUserRole()

#     if userrole == 'admin':
#         return render_template("adminPage.html")
#     elif userrole == None:
#         return redirect(url_for('home'))
#     else:
#         return 'Unauthorised.'

# @app.route("/staffpage")
# def staffPage():
#     if not isAuthenticated():
#         return redirect(url_for('home'))

#     userrole = getUserRole()
#     if userrole == 'staff':
#         return render_template("staffPage.html")
#     elif userrole == None:
#         return redirect(url_for('home'))
#     else:
#         return 'Unauthorised.'

# @app.route("/customerpage")
# def customerPage():
#     if not isAuthenticated():
#         return redirect(url_for('home'))

#     userrole = getUserRole()
#     if userrole == 'customer':
#         return render_template("customerPage.html")
#     elif userrole == None:
#         return redirect(url_for('home'))
#     else:
#         return 'Unauthorised.'


@app.route("/passwordform")
def passwordForm():
    if not isAuthenticated():
        return redirect(url_for('home'))

    return render_template("passwordForm.html")

@app.route("/updatepassword", methods=['GET', 'POST'])
def updatePassword():
    if not isAuthenticated():
        return redirect(url_for('home'))
    msg = ''
    if (request.method == 'POST' 
        and request.form.get('pw') 
        and request.form.get('confirmpw')):

        pw = request.form['pw']
        confirmpw = request.form['confirmpw']

        if pw == confirmpw:
            hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE users SET UserPassword = %s WHERE Username = %s;',(hashed, session['username']))
            mysql.connection.commit()
            msg = 'You have successfully updated your password!'
        else:
            msg = 'Passwords do not match. Please try again.'
    else:
        msg = 'Please fill out the form.'
    return msg

@app.route("/userform/<userrole>")
def userForm(userrole):
    if not isAuthenticated():
        return redirect(url_for('home'))

    user_role = getUserRole()
    if user_role == 'admin' and userrole in ['customer', 'staff']:
        return render_template("userForm.html", userrole=userrole)
    elif user_role == 'admin':
        return "You can either add a 'customer' or 'staff'."
    return "Unauthorised."

@app.route("/addusers/<userrole>", methods=['GET', 'POST'])
def addUsers(userrole):
    if not isAuthenticated():
        return redirect(url_for('home'))
    user_role = getUserRole()
    if user_role == 'admin' and userrole in ['customer', 'staff']:
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
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # print(hashed)
                cursor.execute('INSERT INTO users (Username, UserPassword, UserRole, FirstName, LastName, Address, Email, Phone) \
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (username, hashed, userrole, firstname, lastname, address, email, phone,))
                mysql.connection.commit()
                msg = f'You have successfully added a {userrole}!'
        
        elif request.method == 'POST':
            # Form is empty (no POST data)
            msg = 'Please fill out the form.'
    elif user_role == 'admin':
        msg = "You can either add a 'customer' or 'staff'."
    msg = 'Unauthorised.'
    return msg
    
@app.route("/customerlist/<access>")
def customerList(access):
    if not isAuthenticated():
        return redirect(url_for('home'))
    
    user_role = getUserRole()
    if user_role in ['admin', 'staff'] and access in ['adminaccess', 'staffaccess']:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE UserRole = "customer"')
        account = cursor.fetchall()
        return render_template("customerList.html", account=account, access=access)
    return 'Unauthorised.'

@app.route("/customerinfo/<username>")
def customerInfo(username):
    if not isAuthenticated():
        return redirect(url_for('home'))
    
    user_role = getUserRole()
    if user_role == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
        account = cursor.fetchone()
        return render_template("customerInfo.html", account=account)
    return 'Unauthorised.'


@app.route("/updatecustomer", methods=['GET', 'POST'])
def updateCustomer():
    if not isAuthenticated():
        return redirect(url_for('home'))
    userrole = getUserRole()
    if userrole == 'admin':
        msg = ''
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
    return "Unauthorised."

@app.route("/deletecustomer", methods=['GET', 'POST'])
def deleteCustomers():
    if not isAuthenticated():
        return redirect(url_for('home'))
    userrole = getUserRole()
    if userrole == 'admin':
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM users WHERE Username = %s', (username,))
        mysql.connection.commit()
        msg = 'You have successfully deleted a customer!'
    msg = "Unauthorised."
    return msg





# access control from here 



@app.route("/stafflist")
def staffList():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE UserRole = "staff"')
    account = cursor.fetchall()
    return render_template("staffList.html", account=account)

@app.route("/staffinfo/<username>")
def staffInfo(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
    account = cursor.fetchone()
    return render_template("staffInfo.html", account=account)

@app.route("/updatestaff", methods=['GET', 'POST'])
def updateStaff():
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
            msg = 'You have successfully updated a staff!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    return msg

@app.route("/deletestaff", methods=['GET', 'POST'])
def deleteStaff():
    username = request.form['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM users WHERE Username = %s', (username,))
    mysql.connection.commit()
    msg = 'You have successfully deleted a staff!'
    return msg



@app.route("/carlist/<access>")
def carList(access):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM rental_cars')
    account = cursor.fetchall()
    return render_template("carList.html", account=account, access=access)

@app.route("/carform")
def carForm():
    return render_template("carForm.html")

@app.route("/addcars", methods=['GET', 'POST'])
def addCars():
    msg = ""
    if (request.method == 'POST' 
        and request.form.get('registration') 
        and request.form.get('model') 
        and request.form.get('productionyear') 
        and request.form.get('seating') 
        and request.form.get('rental')):
       
        registration = request.form['registration']
        model = request.form['model']
        productionyear = request.form['productionyear']
        seating = request.form['seating']
        rental = request.form['rental']

        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM rental_cars WHERE Registration = %s', (registration,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists.'
        elif not re.match(r'[A-Za-z0-9]+', registration):
            msg = 'Registration must contain only characters and numbers.'
        elif not re.match(r'^[A-Za-z0-9\s\-]+$', model):
            msg = 'Model must contain only characters, numbers, spaces, and hyphens.'
        
 
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
           
            cursor.execute('INSERT INTO rental_cars (Registration, CarModel, ProductionYear, Seating, RentalPerDay) \
                            VALUES (%s, %s, %s, %s, %s);', (registration, model, productionyear, seating, rental,))
            mysql.connection.commit()
            msg = f'You have successfully added a car!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    return msg



@app.route("/carinfo/<carid>")
def carInfo(carid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM rental_cars WHERE CarID = %s;', (carid,))
    account = cursor.fetchone()
    return render_template("carInfo.html", account=account)

@app.route("/updatecar", methods=['GET', 'POST'])
def updateCar():
    msg = ""
    if (request.method == 'POST' 
        and request.form.get('registration') 
        and request.form.get('model') 
        and request.form.get('productionyear') 
        and request.form.get('seating') 
        and request.form.get('rental')):

        registration = request.form['registration']
        model = request.form['model']
        productionyear = request.form['productionyear']
        seating = request.form['seating']
        rental = request.form['rental']
    
        if not re.match(r'^[A-Za-z0-9\s\-]+$', model):
            msg = 'Model must contain only characters, numbers, spaces, and hyphens.'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE rental_cars SET CarModel = %s, ProductionYear= %s, Seating= %s, RentalPerDay= %s WHERE Registration = %s;',
                            (model, productionyear, seating, rental, registration))
            mysql.connection.commit()
            msg = 'You have successfully updated a car!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    return msg

@app.route("/deletecar", methods=['GET', 'POST'])
def deleteCar():
    carid = request.form['carid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM rental_cars WHERE CarID = %s', (carid,))
    mysql.connection.commit()
    msg = 'You have successfully deleted a car!'
    return msg

@app.route("/displayprofile")
def displayProfile():
    userid = session['id'] 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE UserID = %s;', (userid,))
    account = cursor.fetchone()
    return render_template("profile.html", account=account)


@app.route("/updateprofile", methods=['GET', 'POST'])
def updateProfile():
    msg = ""
    if (request.method == 'POST' 
        and request.form.get('username') 
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
            msg = 'You have successfully updated your profile!'
    elif request.method == 'POST':
        # Form is empty (no POST data)
        msg = 'Please fill out the form.'
    return msg

