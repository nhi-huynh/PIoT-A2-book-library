# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
# from flask_api import api, db
from flask_site import site
from flask_api_book import api as book_api
from flask_api_book import db as book_db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Update HOST and PASSWORD appropriately.
HOST = "35.189.60.60"
USER = "root"
PASSWORD = "piot"
DATABASE = "Library"       #Database name

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

book_db.init_app(app)

app.register_blueprint(book_api)
app.register_blueprint(site)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
