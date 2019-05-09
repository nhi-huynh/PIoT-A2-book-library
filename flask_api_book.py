from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Book(db.Model):
    __tablename__ = "Book"
    ISBN = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text, nullable=False)
    Author = db.Column(db.Text, nullable=False)
    YearPublished = db.Column(db.Integer, nullable=False)
    # Username = db.Column(db.String(256), unique = True)

    def __init__(self, Title, Author, YearPublished):
        # self.ISBN = ISBN
        self.Title = Title
        self.Author = Author
        self.YearPublished = YearPublished

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("ISBN", "Title", "Author", "YearPublished")

bookSchema = BookSchema()
booksSchema = BookSchema(many = True)

# Endpoint to show all books.
@api.route("/books", methods = ["GET"])
def getPeople():
    book = Book.query.all()
    result = booksSchema.dump(book)
    print (result)
    return jsonify(result.data)

# Endpoint to get book by isbn.
@api.route("/books/<isbn>", methods = ["GET"])
def getBook(isbn):
    book = Book.query.get(isbn)

    return bookSchema.jsonify(book)

# Endpoint to create new book.
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
@api.route("/book_update/<isbn>", methods = ["PUT"])
def bookUpdate(isbn):
    book = Book.query.get(isbn)

    title = request.json["title"]
    author = request.json["author"]
    yearPublished = request.json["yearPublished"]

    print("Title to update: {}".format(title))
    print("Author to update: {}".format(author))
    print("YearPublished to update: {}".format(yearPublished))

    book.Title = title
    book.Author = author
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
