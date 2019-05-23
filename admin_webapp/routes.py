# vim: set et sw=4 ts=4 sts=4:
from class_.Auth import Auth
from flask import redirect, session, render_template, request, jsonify
from flask_wtf import FlaskForm
import wtforms as wtf
from run import app, db
from api import ma, Book, BookSchema, Borrow, BorrowSchema

bookSchema = BookSchema()
booksSchema = BookSchema(many=True)
borrowSchema = BorrowSchema()
borrowsSchema = BorrowSchema(many=True)


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
# 	"author": "Eric Ries",
# 	"yearPublished": 2011
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

    title = request.form["title"]
    author = request.form["author"]
    yearPublished = request.form["yearPublished"]

    newBook = Book(
        Title=title, Author=author, YearPublished=yearPublished)
    db.session.add(newBook)
    db.session.commit()

    return bookSchema.jsonify(newBook)

# Endpoint to update book.
# Send a PUT json as below
# {
# 	"title": "The Lean Startup",
# 	"author": "Eric Ries",
# 	"yearPublished": 2012
# }
# If we don't want to change a field, just assign that field to an empty string
# e.g. "title": ""
# The code below will automatically filter out which fields will be changed
# in the db and which is not


@app.route("/api/book/<isbn>", methods=["PUT"])
def bookEdit(isbn):
    """
    A function created to edit a book

    Args:
        isbn: isbn of the book to be edited

    Returns:
        JSON response
    """

    book = Book.query.get(isbn)

    title = request.form["title"]
    author = request.form["author"]
    yearPublished = request.form["yearPublished"]

    if (title != ""):
        book.Title = title
    if (author != ""):
        book.Author = author
    if (yearPublished != ""):
        book.YearPublished = yearPublished

    db.session.commit()

    return bookSchema.jsonify(book)


# Endpoint to delete a book.
@app.route("/api/book/<isbn>", methods=["DELETE"])
def bookDelete(isbn):
    """
    A function created to delete a book

    Args:
        isbn: isbn of the book to be deleted

    Returns:
        JSON response
    """

    book = Book.query.get(isbn)

    db.session.delete(book)
    db.session.commit()

    return bookSchema.jsonify(book)


# Endpoint to show all borrows.
@app.route("/api/borrow", methods=["GET"])
def getBorrows():
    """
    A function created to get  borrowed books

    Returns:
        JSON response
    """

    borrow = Borrow.query.all()
    result = borrowsSchema.dump(borrow)
    return jsonify(result.data)


# Endpoint to get borrow by borrowID.
@app.route("/api/borrow/<id>", methods=["GET"])
def getborrow(id):
    """
    A function created to find a borrowed book

    Args:
        id: ID of the borrowed book to be found

    Returns:
        JSON response
    """

    borrow = Borrow.query.get(id)

    return borrowSchema.jsonify(borrow)


# Endpoint to create new borrow.
@app.route("/api/borrow", methods=["POST"])
def addborrow():
    """
    A function created to add a borrowed book

    Args:
        borrowID: ID of the borrowed book to be added

    Returns:
        JSON response
    """

    isbn = request.form["ISBN"]
    username = request.form["username"]

    newBorrow = Borrow(isbn=isbn, username=username)
    db.session.add(newBorrow)
    db.session.commit()

    return borrowSchema.jsonify(newBorrow)


# Endpoint to update borrow.
@app.route("/api/borrow/<borrowID>", methods=["PUT"])
def borrowUpdate(borrowID):
    """
    A function created to update a borrowed book

    Args:
        borrowID: ID of the borrowed book to be updates

    Returns:
        JSON response
    """

    borrow = Borrow.query.get(borrowID)

    ISBN = request.form["ISBN"]
    username = request.form["username"]
    borrowDate = request.form["borrowDate"]
    dueDate = request.form["borrowDate"]
    returnDate = request.form["returnDate"]
    eventID = request.form["eventID"]

    print("ISBN to update: {}".format(ISBN))
    print("username to update: {}".format(username))
    print("borrowDate to update: {}".format(borrowDate))
    print("dueDate to update: {}".format(dueDate))
    print("returnDate to update: {}".format(returnDate))
    print("eventID to update: {}".format(eventID))

    borrow.ISBN = ISBN
    borrow.username = username
    borrow.borrowDate = borrowDate
    borrow.dueDate = dueDate
    borrow.returnDate = returnDate
    borrow.eventID = eventID

    db.session.commit()

    return borrowSchema.jsonify(borrow)


# Endpoint to delete a borrow.
@app.route("/api/borrow/<borrowID>", methods=["DELETE"])
def borrowDelete(borrowID):
    """
    A function created to delete a borrowed book

    Args:
        borrowID: ID of the borrowed book to be removed

    Returns:
        JSON response
    """

    borrow = Borrow.query.get(borrowID)

    db.session.delete(borrow)
    db.session.commit()

    return borrowSchema.jsonify(borrow)


# Endpoint to get weekly borrows
@app.route("/api/borrow/weekly", methods=["GET"])
def getWeeklyBorrow():
    now = date.today()
    seven_days_ago = now - timedelta(days=7)

    weeklyBorrow = Borrow.query.filter(
        func.date(Borrow.borrowDate) > seven_days_ago).all()
    result = borrowsSchema.dump(weeklyBorrow)    
    return jsonify(result.data)


# Endpoint to get daily borrows
@app.route("/api/borrow/daily", methods=["GET"])
def getDailyBorrow():
    dailyBorrow = Borrow.query.filter(
        func.date(Borrow.borrowDate) == func.date(func.current_date())).all()

    result = borrowsSchema.dump(dailyBorrow)    
    return jsonify(result.data)


# Endpoint to get currently borrowed books
@app.route("/api/borrow/current", methods=["GET"])
def getCurrentBorrow():
    currentBorrow = Borrow.query.filter(Borrow.returnDate.is_(None)).all()
    result = borrowsSchema.dump(currentBorrow)

    return jsonify(result.data)


@app.route('/admin/daily-borrows')
def daily_borrows():
    if not logged_in(session):
        return redirect('/login')
    
    return render_template('admin-dashboard.bs.html', page='dashboard')
