# Only True during development
DEBUG = True

# Required
# One way to generate is by grabbing the output of python's os.urandom(16)
# You may use a value > 16
# Values lower are not recommended as they aren't as secure
SECRET_KEY = b'Secret here'

# Run /admin_webapp/gen_admin_pw.py
ADMIN_USERNAME = 'username'
ADMIN_PASSWORD = b'password cipher'

# This is the db that contains all library data
DB_HOST = "localhost"
DB_USER = "username"
DB_PASSWORD = "password"
DB_DATABASE = "DB_name"

# Do not change this
SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_DATABASE
)

# Recommended True
SQLALCHEMY_TRACK_MODIFICATIONS = True
