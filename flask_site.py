from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
def index():
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/books")
    data = json.loads(response.text)

    return render_template("index.html", books = data)

# Client webpage.
@site.route("/all_borrows")
def borrows_index():
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/borrows")
    data = json.loads(response.text)

    return render_template("borrows_index.html", borrows = data)