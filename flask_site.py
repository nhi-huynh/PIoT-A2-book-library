from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import requests
import json

site = Blueprint("site", __name__)


# Client webpage.
@site.route("/")
def index():
    """
    A function created to create the client webpage

    Returns:
        Template
    """
    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/books")
    data = json.loads(response.text)

    return render_template("index.html", books=data)


# Client webpage.
@site.route("/all_borrows")
def borrows_index():
    """
    A function created to get borrows index

    Returns:
        Template
    """

    # Use REST API.
    response = requests.get("http://127.0.0.1:5000/borrows")
    data = json.loads(response.text)

    return render_template("borrows_index.html", borrows=data)
