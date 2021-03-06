from app import app
from app.models import *
from flask import request

def get_user_by_string(string, pid):
	return User.query.filter(User.name==string).filter(User.panlist_id==pid).first()

def is_user_by_num(num, pid):
	if User.query.filter(User.number==num).filter(User.panlist_id==pid).first() is not None:
		return True
	return False

def is_user_by_string(string, pid):
	if get_user_by_string(string, pid) is not None:
		return True
	return False

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')