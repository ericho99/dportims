from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

from flask_cas import CAS
CAS(app)
app.config['CAS_SERVER'] = 'https://secure.its.yale.edu'
app.config['CAS_LOGIN_ROUTE'] = '/cas/login'
app.config['CAS_AFTER_LOGIN'] = '/index'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASK_DATABASE_URL']
db = SQLAlchemy(app)

from app import views, models