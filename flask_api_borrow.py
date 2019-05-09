from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from datetime import datetime, date, timedelta

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Borrow(db.Model):
    __tablename__ = "Borrow"
    borrowID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ISBN = db.Column(db.Integer, db.ForeignKey("Book.ISBN"))
    username = db.Column(db.Text, nullable=False)
    borrowDate = db.Column(db.DateTime, nullable=False)
    dueDate = db.Column(db.DateTime, nullable=False)
    returnDate = db.Column(db.DateTime)
    eventID = db.Column(db.Text)
    book = db.relationship("Book", backref="borrows")

    def __init__(self, isbn, username):
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
        # Fields to expose.
        fields = ("borrowID", "username", "borrowDate", "dueDate", "returnDate", "eventID")

borrowSchema = BorrowSchema()
borrowsSchema = BorrowSchema(many = True)

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
