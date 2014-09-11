from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class UserForm(Form):
    name = TextField('name', validators = [Required()])
    email = TextField('email', validators = [Required()])
    number = TextField('number', validators = [Required()])