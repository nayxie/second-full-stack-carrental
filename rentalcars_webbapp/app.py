from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def logIn():
    return render_template("logIn.html")

@app.route("/checkid", methods=["POST"])
def checkID():
    username = request.form.get("username")
    password = request.form.get("password")
    return f"hello {username} pw {password} check ID in progress"
# route and function here to deal with log in information
# fetch username and password 
# if usermname doesn't exist, or username and pw don't match, display msg
# if correct, display a message "welcome {firstname lastname}! role: {role}"
# display links accordingly 


