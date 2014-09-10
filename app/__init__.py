from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

from flask.ext.cas import CAS
cas = CAS(app)
app.config['CAS_SERVER'] = 'https://secure.its.yale.edu'
app.config['CAS_LOGIN_ROUTE'] = '/cas/login'
app.config['CAS_AFTER_LOGIN'] = 'index'
app.config['SECRET_KEY'] = os.environ['USER_AUTH_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASK_DATABASE_URL']
db = SQLAlchemy(app)

from app import views, models