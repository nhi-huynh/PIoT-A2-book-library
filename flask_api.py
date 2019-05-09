from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Person(db.Model):
    __tablename__ = "Person"
    PersonID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Name = db.Column(db.Text)
    # Username = db.Column(db.String(256), unique = True)

    def __init__(self, Name, PersonID = None):
        self.PersonID = PersonID
        self.Name = Name

class PersonSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("PersonID", "Name")

personSchema = PersonSchema()
personsSchema = PersonSchema(many = True)

# Endpoint to show all people.
@api.route("/person", methods = ["GET"])
def getPeople():
    people = Person.query.all()
    result = personsSchema.dump(people)

    return jsonify(result.data)

# Endpoint to get person by id.
@api.route("/person/<id>", methods = ["GET"])
def getPerson(id):
    person = Person.query.get(id)

    return personSchema.jsonify(person)

# Endpoint to create new person.
@api.route("/person", methods = ["POST"])
def addPerson():
    name = request.json["name"]

    newPerson = Person(Name = name)

    db.session.add(newPerson)
    db.session.commit()

    return personSchema.jsonify(newPerson)

# Endpoint to update person.
@api.route("/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = request.json["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person)
