import os
import requests

from flask import Flask, session, render_template, request, jsonify, flash, redirect, url_for, logging
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='mdbootstrap')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://ipsasfucoadidx:87e404320b8d48f6ec3d84c8104e0bf211d5b12e698ea1b2916f754f03272489@ec2-54-217-224-85.eu-west-1.compute.amazonaws.com:5432/de3bfes1n10hdc")
db = scoped_session(sessionmaker(bind=engine))

# Create database tables
def users_table():
    db.execute("""CREATE TABLE users (id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL, username VARCHAR NOT NULL, password VARCHAR NOT NULL);""")

def books():
    db.execute("""CREATE TABLE books (title VARCHAR NOT NULL,
    author VARCHAR NOT NULL, year VARCHAR NOT NULL, isbn VARCHAR NOT NULL,
    review_count INTEGER NOT NULL, average_score DECIMAL NOT NULL);""")

def reviews():
    db.execute("""CREATE TABLE reviews (rating INTEGER,
    review_message VARCHAR, date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, book_isbn VARCHAR REFERENCES imported_books, user_id INTEGER REFERENCES users);""")

@app.template_filter('datetimeformat')
def datetimeformat(value, format = '%B'):
    return value.strftime(format)

# Search function
def search():
    if request.method == 'POST' and "searchData" in request.form:
        data = request.form.get("searchData")
        search_choice = request.form.get("search_choice")
        print(data)
        if data == '':
            flash('Please type something before searching.', 'error')
        else:
            if str(search_choice) == 'isbn':
                books = db.execute("SELECT * FROM imported_books WHERE (isbn LIKE :data)",
                                {"data": '%' + data + '%'}).fetchall()
            elif str(search_choice) == 'title':
                books = db.execute("SELECT * FROM imported_books WHERE (title LIKE :data)",
                                {"data": '%' + data + '%'}).fetchall()
            elif str(search_choice) == 'author':
                books = db.execute("SELECT * FROM imported_books WHERE (author LIKE :data)",
                                {"data": '%' + data + '%'}).fetchall()
            else:
                books = db.execute("""SELECT * FROM imported_books WHERE
                    (isbn LIKE :data) OR (title LIKE :data)
                    OR (author LIKE :data)""",
                    {"data": '%' + data + '%'}).fetchall()
            if not books:
                flash('No results found  ¯\_(ツ)_/¯', 'error')
            else:
                return books

# Main route
@app.route("/")
def index():
    return render_template("index.html")

# Register route
@app.route("/register", methods=['GET', "POST"])
def register():
    session.clear()
    if request.method == 'POST':
        users = db.execute("SELECT * FROM users").fetchall()
        name = request.form.get("name")
        username = request.form.get("username")
        password = sha256_crypt.encrypt(str(request.form.get("password")))
        notencryptedpass = request.form.get("password")
        errors = []

        for user in users:
            if username == user.username:
                error1 = 'Username already in use!'
                errors.append(error1)

        if not(username) or not(name) or not(notencryptedpass):
            error2 = 'Please fill in all the fields!'
            errors.append(error2)

        if len(str(notencryptedpass)) < 6:
            error3 = 'Password should be at least 6 characters!'
            errors.append(error3)

        if len(errors) > 0:
            return render_template('register.html', errors=errors)
        else:
            db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
                    {"name": name, "username": username, "password": password})
            db.commit()
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get("username")
        password_candidate = request.form.get("password")
        result = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username}).fetchone()
        errors = []

        if result is not None:
            if sha256_crypt.verify(password_candidate, result['password']):
                session['logged_in'] = True
                session['username'] = username
                session['name'] = result.name
                session['id'] = result.id

                # flash(f'Welcome {result.name} !', 'success')
                # flash('You are now logged in', 'success')

                return redirect(url_for('dashboard', id = session.get("id"), name = session.get("name")))
            else:
                error1 = 'Invalid password'
                errors.append(error1)
                return render_template('login.html', errors = errors)
            db.close()
        else:
            error2 = 'Username not found'
            errors.append(error2)
            return render_template('login.html', errors = errors)

    return render_template('login.html')

# Check if logged in function
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'error')
            return redirect(url_for('login'))
    return wrap

# Logout route
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Main route if logged in
@app.route("/",  methods=['GET', "POST"])
@is_logged_in
def index_logged_in():
    books = search()
    data = request.form.get("searchData")
    if books:
        return render_template('search.html', data = data, books = books)
    return render_template("index.html")

# Dashboard route
@app.route('/dashboard/<name>', methods = ['GET', 'POST'])
@is_logged_in
def dashboard(name):
    books = search()
    data = request.form.get("searchData")
    if books:
        return render_template('search.html', data = data, books = books)
    return render_template('dashboard.html')

# Book details route
@app.route('/dashboard/<name>/books/<isbn>', methods = ['GET', 'POST'])
@is_logged_in
def book(isbn, name):
    book = db.execute("SELECT * FROM imported_books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "saCxBQEHrhQK1AL0EiDg", "isbns": isbn})
    reviews_count = res.json()["books"][0]["reviews_count"]
    average_rating=res.json()["books"][0]["average_rating"]
    reviews = db.execute("SELECT * FROM reviews WHERE reviews.book_isbn=:isbn", {"isbn": isbn}).fetchall()
    id = session.get("id")
    review = db.execute("SELECT user_id FROM reviews WHERE reviews.book_isbn=:isbn AND reviews.user_id=:id", {"isbn": isbn, "id": id}).fetchone()
    user_reviews_count = db.execute("SELECT COUNT(review_message) FROM reviews WHERE reviews.user_id=:id", {"id": id}).fetchall()
    user_of_review = db.execute("SELECT users.username FROM users \
                                INNER JOIN reviews ON users.id=reviews.user_id \
                                WHERE reviews.book_isbn=:isbn", {"isbn": isbn}).fetchone()
    books = search()
    data = request.form.get("searchData")
    if books:
        return render_template('search.html', data = data, books = books)

    if request.method == 'POST' and "review_message" in request.form or "rating" in request.form:
        review_message = request.form.get("review_message")
        rating_value = request.form.get("rating")

        if review is not None:
            flash('You cannot write more than one review :/', 'error')
        elif review_message == '':
            flash('Please type something before submiting :)', 'error')
        elif rating_value is None:
            flash('Please rate the book :)', 'error')
        else:
            db.execute("INSERT INTO reviews (rating, review_message, book_isbn, user_id) VALUES (:rating, :review_message, :book_isbn, :user_id);",
                    {"rating": rating_value, "review_message": review_message, "book_isbn": isbn, "user_id": id})
            db.commit()
            flash('Your review has been added successfully!', 'success')
            return redirect(url_for('book', isbn = book.isbn, name = session.get("name")))

    return render_template('book.html', book=book, reviews = reviews, reviews_count = reviews_count, average_rating = average_rating, user_of_review = user_of_review)

# Get book by isbn api
@app.route('/api/<isbn>')
def isbn_api(isbn):
    book = db.execute("SELECT * FROM imported_books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 422

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "saCxBQEHrhQK1AL0EiDg", "isbns": isbn})
    return jsonify({
        'ISBN': book.isbn,
        'Title': book.title,
        'Author': book.author,
        'year': book.year,
        'reviews_count': res.json()["books"][0]["reviews_count"],
        'average_score': res.json()["books"][0]["average_rating"]
    })

if __name__ == '__main__':
    app.run(debug=True)
