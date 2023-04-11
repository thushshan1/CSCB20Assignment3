from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "icecream123"
app.permanent_session_lifetime = timedelta(minutes=10)

con = sqlite3.connect("database.db")
cur = con.cursor()

sql_query = """
    CREATE TABLE IF NOT EXISTS Member
    (
    username TEXT PRIMARY KEY,
    password TEXT,
    quest TEXT
    )
"""

@app.route('/')
def index():
  return render_template("home.html")

@app.route('/Register', methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        quest = request.form['quest']

        password_hashed = bcrypt.generate_password_hash(password)
        password_hashed_str = password_hashed.decode('utf-8')

        try:
            sql_query = "INSERT INTO User VALUES ('"
            sql_query += username + "','" + password_hashed_str + "','" + quest+ "')"
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute(sql_query)
            con.commit()
            flash("User successfully added")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists")
            return render_template('Register.html')
    else:
        return render_template('Register.html')


    
@app.route('/Login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        session["username"] = username

    return render_template("Login.html")

  



app.run(host='0.0.0.0', port=81, debug=True)