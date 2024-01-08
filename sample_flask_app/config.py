from os import environ
from urllib.parse import quote_plus

DB_USER = environ['DB_USER']
DB_HOST = environ['DB_HOST']
DB_NAME = environ['DB_NAME']
DB_PASSWORD = quote_plus(environ['DB_PASSWORD'])
DB_PORT = environ['DB_PORT']
# Database
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_APP = environ.get("FLASK_APP")
FLASK_ENV = environ.get("FLASK_ENV")
