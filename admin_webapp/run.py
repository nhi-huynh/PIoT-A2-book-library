# vim: set et sw=4 ts=4 sts=4:

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)

app.config.from_object('config')
app.config.from_pyfile('config.py')

import routes

if __name__ == '__main__':
    app.run()
