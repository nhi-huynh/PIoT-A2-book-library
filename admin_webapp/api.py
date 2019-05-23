from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Book(db.Model):
    """
    A class used to declare the book model

    Attributes
    ----------
    ISBN : string
        the isbn of the book
    Title : string
        the Title of the book
    Author : string
        the Author of the book
    YearPublished : int
        the YearPublished of the book

    """

    __tablename__ = "Book"
    ISBN = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.Text, nullable=False)
    Author = db.Column(db.Text, nullable=False)
    YearPublished = db.Column(db.Integer, nullable=False)
    borrows = db.relationship("Borrow", backref="book", lazy=True)

    def __init__(self, Title, Author, YearPublished, ISBN=None):
        """
        A constructor to create a new Book object
        """
        self.ISBN = ISBN
        self.Title = Title
        self.Author = Author
        self.YearPublished = YearPublished


class BookSchema(ma.Schema):
    """A class used to represent the BookSchema"""

    # Reference: https://github.com/marshmallow-code/marshmallow/
    # issues/377#issuecomment-261628415
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        model = Book
        fields = ("ISBN", "Title", "Author", "YearPublished")


# Declaring the Borrow model.
class Borrow(db.Model):
    """
    A class used to declare the borrow Author

    Attributes
    ----------
    borrowID : string
        the id of the book
    ISBN : string
        the isbn of the book
    username : string
        the username of the person borrowing the book
    borrowDate : datetime
        the date and time the book has been borrowed
    dueDate : datetime
        the date and time the book is due to be returned
    returnDate : datetime
        the actual returned date and time
    eventID : string
        the calendar event id string
    """

    __tablename__ = "Borrow"
    borrowID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ISBN = db.Column(db.Integer, db.ForeignKey("Book.ISBN"), nullable=False)
    username = db.Column(db.Text, nullable=False)
    borrowDate = db.Column(db.DateTime, nullable=False)
    dueDate = db.Column(db.DateTime, nullable=False)
    returnDate = db.Column(db.DateTime)
    eventID = db.Column(db.Text)
    # book = db.relationship("Book", backref="borrows")

    def __init__(self, isbn, username, borrowID=None):
        """
        A constructor to create a new Borrow object
        """
        self.borrowID = borrowID
        self.ISBN = isbn
        self.username = username
        self.borrowDate = datetime.now()
        self.dueDate = self.borrowDate + timedelta(days=7)
        self.returnDate = None
        self.eventID = None


class BorrowSchema(ma.Schema):
    """A class used to represent the BorrowSchema"""

    # Reference: https://github.com/marshmallow-code/marshmallow/
    # issues/377#issuecomment-261628415
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        table = Borrow.__table__
        # Fields to expose.
        fields = (
            "borrowID",
            "username",
            "borrowDate",
            "dueDate",
            "returnDate",
            "eventID",
            "book")
   
    book = ma.Nested(BookSchema)
