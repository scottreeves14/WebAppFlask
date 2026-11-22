from flask import Flask, render_template, request, redirect, url_for, session 
import sqlite3 
 
app = Flask(__name__) 
app.secret_key = "secretkey123" 
DATABASE = "database.db"

@app.route('/')
def index():
    return render_template("index.html")

def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor() 
 
    c.execute('''CREATE TABLE IF NOT EXISTS user ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE, 
    email TEXT, 
    password TEXT 
    )''') 
 
    c.execute('''CREATE TABLE IF NOT EXISTS ticket_type ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    price REAL 
    )''') 
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST']) 
def register(): 
    if request.method == 'POST': 
        username = request.form['username'] 
        email = request.form['email'] 
        password = request.form['password'] 
 
        conn = sqlite3.connect(DATABASE) 
        c = conn.cursor() 
        c.execute("SELECT * FROM user WHERE username = ?", (username,)) 
        if c.fetchone(): 
            return "Username already exists." 
 
        c.execute("INSERT INTO user (username, email, password) VALUES (?, ?, ?)", 
        (username, email, password)) 
        conn.commit() 
        conn.close() 
        return redirect(url_for('login')) 
 
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
 
        conn = sqlite3.connect(DATABASE) 
        c = conn.cursor() 
        c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password)) 
        user = c.fetchone() 
        conn.close() 
 
        if user: 
            session['user'] = username 
            return redirect(url_for('index')) 
        else: 
            return "Invalid login details." 
    return render_template('login.html')

@app.route('/logout') 
def logout():
    session.pop('user', None) 
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)