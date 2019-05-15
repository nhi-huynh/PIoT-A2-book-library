from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from datetime import datetime, date, timedelta
from sqlalchemy import func


api = Blueprint("library_api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

class Book(db.Model):
    """
    Declaring the Book model by declaring all existing fields 
    """
    __tablename__ = "Book"
    ISBN = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text, nullable=False)
    Author = db.Column(db.Text, nullable=False)
    YearPublished = db.Column(db.Integer, nullable=False)
    borrows = db.relationship("Borrow", backref="book", lazy=True)

    def __init__(self, Title, Author, YearPublished, ISBN = None):
        """
        A constructor to create a new Book object  
        """
        self.ISBN = ISBN
        self.Title = Title
        self.Author = Author
        self.YearPublished = YearPublished

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        model = Book
        fields = ("ISBN", "Title", "Author", "YearPublished")

bookSchema = BookSchema()
booksSchema = BookSchema(many = True)


# Declaring the Borrow model.
class Borrow(db.Model):
    """
    Declaring the Borrow model by declaring all existing fields 
    """
    __tablename__ = "Borrow"
    borrowID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ISBN = db.Column(db.Integer, db.ForeignKey("Book.ISBN"), nullable=False)
    username = db.Column(db.Text, nullable=False)
    borrowDate = db.Column(db.DateTime, nullable=False)
    dueDate = db.Column(db.DateTime, nullable=False)
    returnDate = db.Column(db.DateTime)
    eventID = db.Column(db.Text)
    #book = db.relationship("Book", backref="borrows")

    def __init__(self, isbn, username, borrowID = None):
        """
        A constructor to create a new Borrow object  
        """
        self.borrowID = borrowID
        self.ISBN = isbn
        self.username = username
        self.borrowDate = date.today()
        self.dueDate = date.today() + timedelta(days=7)
        self.returnDate = None
        self.eventID = None

class BorrowSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        table = Borrow.__table__
        # Fields to expose.
        fields = ("borrowID", "username", "borrowDate", "dueDate", "returnDate","ISBN","eventID", "book")
   
    book = ma.Nested(BookSchema)

borrowSchema = BorrowSchema()
borrowsSchema = BorrowSchema(many = True)


# Endpoint to show all books.
@api.route("/books", methods = ["GET"])
def getBooks():
    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)

# Endpoint to get book by isbn.
@api.route("/books/<isbn>", methods = ["GET"])
def getBookByISBN(isbn):
    book = Book.query.get(isbn)

    return bookSchema.jsonify(book)

# Endpoint to create new book.
# Send a POST json as below
# {
# 	"title": "The Lean Startup",
# 	"author": "Eric Ries",
# 	"yearPublished": 2011
# }
@api.route("/book_new", methods = ["POST"])
def addBook():
    title = request.json["title"]
    author = request.json["author"]
    yearPublished = request.json["yearPublished"]
    
    newBook = Book(Title = title, Author = author, YearPublished = yearPublished)
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
# If we don't want to change a field, just assign that field to an empty string.
# e.g. "title": ""
# The code below will automatically filter out which fields will be changed in the db 
# and which is not 
@api.route("/book_edit/<isbn>", methods = ["PUT"])
def bookEdit(isbn):
    book = Book.query.get(isbn)

    title = request.json["title"]
    author = request.json["author"]
    yearPublished = request.json["yearPublished"]

    if (title != ""):
        book.Title = title
    if (author != ""):
        book.Author = author
    if (yearPublished != ""):
        book.YearPublished = yearPublished

    db.session.commit()

    return bookSchema.jsonify(book)

# Endpoint to delete a book.
@api.route("/book_delete/<isbn>", methods = ["DELETE"])
def bookDelete(isbn):
    book = Book.query.get(isbn)

    db.session.delete(book)
    db.session.commit()

    return bookSchema.jsonify(book)

# Endpoint to show all borrows.
@api.route("/borrows", methods = ["GET"])
def getBorrows():
    borrow = Borrow.query.all()
    result = borrowsSchema.dump(borrow)
    print (result)
    return jsonify(result.data)

# Endpoint to get borrow by borrowID.
@api.route("/borrows/<id>", methods = ["GET"])
def getborrow(id):
    borrow = Borrow.query.get(id)

    return borrowSchema.jsonify(borrow)

# Endpoint to create new borrow.
@api.route("/borrow_new", methods = ["POST"])
def addborrow():
    isbn = request.json["ISBN"]
    username = request.json["username"]

    newBorrow = Borrow(isbn = isbn, username = username)
    db.session.add(newBorrow)
    db.session.commit()

    return borrowSchema.jsonify(newBorrow)

# Endpoint to update borrow.
@api.route("/borrow_update/<borrowID>", methods = ["PUT"])
def borrowUpdate(borrowID):
    borrow = Borrow.query.get(borrowID)

    ISBN = request.json["ISBN"]
    username = request.json["username"]
    borrowDate = request.json["borrowDate"]
    dueDate = request.json["borrowDate"]
    returnDate = request.json["returnDate"]
    eventID = request.json["eventID"]

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
@api.route("/borrow_delete/<borrowID>", methods = ["DELETE"])
def borrowDelete(borrowID):
    borrow = Borrow.query.get(borrowID)

    db.session.delete(borrow)
    db.session.commit()

    return borrowSchema.jsonify(borrow)

# Endpoint to get weekly borrows
@api.route("/borrows/weekly", methods=["GET"])
def getWeeklyBorrow():
    now = date.today()
    seven_days_ago = now - timedelta(days=7)

    weeklyBorrow = Borrow.query.filter(func.date(Borrow.borrowDate) > seven_days_ago).all()
    # weeklyBorrow = Session.query(Book, Borrow).filter(Book.ISBN == Borrow.ISBN).filter(func.date(Borrow.borrowDate) > seven_days_ago).all()
    result = borrowsSchema.dump(weeklyBorrow)    
    return jsonify(result.data)


# Endpoint to get daily borrows
@api.route("/borrows/daily", methods=["GET"])
def getDailyBorrow():
    dailyBorrow = Borrow.query.filter(func.date(Borrow.borrowDate) == func.date(func.current_date())).all()

    result = borrowsSchema.dump(dailyBorrow)    
    return jsonify(result.data)


# Endpoint to get currently borrowed books
@api.route("/borrows/current", methods=["GET"])
def getCurrentBorrow():
    currentBorrow = Borrow.query.filter(Borrow.returnDate.is_(None)).all()
    result = borrowsSchema.dump(currentBorrow)

    return jsonify(result.data)
