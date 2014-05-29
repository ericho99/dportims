from app import app
from app.models import *

INITLIST = {
    # "+15038872891": "Eric",
    "+15038939333": "ericcc",
    # "+13037178692": "Maren",
    # "+13048905251": "Connor",
    # "+17082978240": "Julianne",
    # "+16107375637": "Claire",
    # "+16086954412": "Fabi",
}

db.drop_all()
db.create_all()

p = Panlist(name='textlist')
db.session.add(p)

for num in INITLIST:
	u = User(number=num,name=INITLIST[num],admin=1,panlist=p)
	db.session.add(u)

db.session.commit()

