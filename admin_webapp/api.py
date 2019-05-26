from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.mysql import BIGINT

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
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ISBN = db.Column(BIGINT, unique=True)
    Title = db.Column(db.Text, nullable=False)
    Author = db.Column(db.Text, nullable=False)
    YearPublished = db.Column(db.Integer, nullable=False)

    def __init__(self, ISBN, Title, Author, YearPublished, BookID=None):
        """
        A constructor to create a new Book object
        """
        self.BookID = BookID
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
        fields = ("BookID", "ISBN", "Title", "Author", "YearPublished")
