from flask import Flask
import os
# from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASK_DATABASE_URL']
db = SQLAlchemy(app)

from app import views, models