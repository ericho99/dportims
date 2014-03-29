from app import app
from app.models import *

db.drop_all()
db.create_all()

p = Panlist(name='textlist')
db.session.add(p)
db.session.commit()

