# vim: set et sw=4 ts=4 sts=4:
from class_.Auth import Auth
from flask import redirect, session, render_template, request, jsonify
from flask_wtf import FlaskForm
import wtforms as wtf
from run import app, db
from api import ma, Book, BookSchema

bookSchema = BookSchema()
booksSchema = BookSchema(many=True)


def logged_in(sess):
    return 'auth_success' in sess and sess['auth_success']


class LoginForm(FlaskForm):
    uname = wtf.TextField('Username', [wtf.validators.required()])
    password = wtf.PasswordField('Password', [wtf.validators.required()])
    submit = wtf.SubmitField('Submit')


@app.route('/')
@app.route('/index')
def index():
    if logged_in(session):
        return redirect('/admin')

    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in(session):
        return redirect('/admin')

    if request.method == 'GET' or 'ajax' not in request.form:
        form = LoginForm()
        return render_template('login.bs.html', form=form)

    if 'user' not in request.form or 'pass' not in request.form:
        return '{"auth_succes":false}'

    user = request.form['user']
    pass_ = request.form['pass']

    if not Auth.verify_passwd(pass_, app.config['ADMIN_PASSWORD']):
        return '{"auth_succes":false}'

    if user != app.config['ADMIN_USERNAME']:
        return '{"auth_success":false}'

    session['auth_success'] = True

    return '{"auth_success":true}'


@app.route('/logout')
def logout():
    if 'auth_success' in session:
        del session['auth_success']

    return redirect('/login')


@app.route('/admin')
@app.route('/admin/dashboard')
def dashboard():
    if not logged_in(session):
        return redirect('/login')

    return render_template('admin-dashboard.bs.html', page='dashboard')


@app.route('/admin/book-manager')
def book_manage():
    if not logged_in(session):
        return redirect('/login')
    
    return render_template('admin-book-manager.bs.html', page='manage')


#
# API
#

# Endpoint to show all books.
@app.route("/api/book", methods=["GET"])
def getBooks():
    """
    A function created to find all books

    Returns:
        JSON response
    """

    if not logged_in(session):
        return redirect('/login')

    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)


# Endpoint to get book by isbn.
@app.route("/api/book/<isbn>", methods=["GET"])
def getBookByISBN(isbn):
    """
    A function created to find a book by its ISBN

    Args:
        isbn: isbn of the book to be found

    Returns:
        JSON response
    """

    book = Book.query.get(isbn)

    return bookSchema.jsonify(book)


# Endpoint to create new book.
# Send a POST json as below
# {
#     "title": "The Lean Startup",
#     "author": "Eric Ries",
#     "yearPublished": 2011
# }
@app.route("/api/book", methods=["POST"])
def addBook():
    """
    A function created to add a book

    Args:
        isbn: isbn of the book to be added

    Returns:
        JSON response
    """

    isbn = request.form['isbn']
    title = request.form["title"]
    author = request.form["author"]
    yearPublished = request.form["yearPublished"]

    newBook = Book(
        ISBN=isbn,
        Title=title,
        Author=author,
        YearPublished=yearPublished
    )

    db.session.add(newBook)
    db.session.commit()

    return bookSchema.jsonify(newBook)

# Endpoint to update book.
# Send a PUT json as below
# {
#     "title": "The Lean Startup",
#     "author": "Eric Ries",
#     "yearPublished": 2012
# }
# If we don't want to change a field, just assign that field to an empty string
# e.g. "title": ""
# The code below will automatically filter out which fields will be changed
# in the db and which is not


@app.route("/api/book/<bookid>", methods=["PUT"])
def bookEdit(bookid):
    """
    A function created to edit a book

    Args:
        isbn: isbn of the book to be edited

    Returns:
        JSON response
    """

    book = Book.query.get(bookid)

    isbn = request.form["isbn"]
    title = request.form["title"]
    author = request.form["author"]
    yearPublished = request.form["yearPublished"]

    if (isbn != ""):
        book.ISBN = isbn
    if (title != ""):
        book.Title = title
    if (author != ""):
        book.Author = author
    if (yearPublished != ""):
        book.YearPublished = yearPublished

    db.session.commit()

    return bookSchema.jsonify(book)


# Endpoint to delete a book.
@app.route("/api/book/<bookid>", methods=["DELETE"])
def bookDelete(bookid):
    """
    A function created to delete a book

    Args:
        isbn: isbn of the book to be deleted

    Returns:
        JSON response
    """

    book = Book.query.get(bookid)

    db.session.delete(book)
    db.session.commit()

    return bookSchema.jsonify(book)
