# TODO False when project done
DEBUG = True

SECRET_KEY = b'Secret here'

ADMIN_USERNAME = 'username'
ADMIN_PASSWORD = b'password cipher'

PLOTLY_USERNAME = 'user'
PLOTLY_API_KEY = 'key'

DB_HOST = "localhost"
DB_USER = "username"
DB_PASSWORD = "password"
DB_DATABASE = "DB_name"

SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_DATABASE
)

SQLALCHEMY_TRACK_MODIFICATIONS = True
