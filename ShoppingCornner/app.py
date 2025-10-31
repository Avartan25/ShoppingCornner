from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import datetime
from passlib.hash import sha256_crypt
from urllib.parse import quote
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a_default_backup_key') # Better for production

# Get the single database URL from the environment variable
DATABASE_URL = os.environ.get('postgresql://shoppingcorner_db_user:Ajr4vR8rmeXP6pNIca956iLjpTvEQE3u@dpg-d3vo2vali9vc73bekjp0-a/shoppingcorner_db')

# Fix for Render/Heroku's 'postgres://' prefix
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------- MODELS ----------
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    PN = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    state_city = db.Column(db.String(255))
    pincode = db.Column(db.String(10))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(300), nullable=False)

# ---------- ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if user and sha256_crypt.verify(password, user.password):
            session['email'] = email
            return render_template('home.html')
        else:
            return render_template('login.html', message="Invalid email or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        epassword = sha256_crypt.hash(password)

        dataentry = Users(
            fullname=request.form['fullname'],
            email=request.form['email'],
            PN=request.form['PN'],
            password=epassword,
            address=request.form['address'],
            state_city=request.form['state_city'],
            pincode=request.form['pincode']
        )
        try:
            db.session.add(dataentry)
            db.session.commit()
            return render_template('login.html', message="You have registered successfully")
        except Exception as e:
            print("Error:", e)
            return render_template('registration.html', msg="Something went wrong, try again")

    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/category')
def category():
    return render_template('Chategory.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact(): 
    if request.method == 'POST':
        entry = Contact(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        try:
            db.session.add(entry)
            db.session.commit()
            print("Message saved successfully")
        except Exception as e:
            print("Error:", e)

    return render_template('contact.html')

@app.route('/profile_page')
def profile():
    return render_template('profile.html')

@app.route('/cart')
def cart():
    return "Cart Page Under Development"

@app.route('/admin')
def admin():
    return render_template('admin.html')
# ---------- MAIN ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # <-- Create tables if not exist
    app.run(debug=True)
