from app import app
from app.models import *
from datetime import datetime

g1=Game(sport=18,date=datetime(2014,12,4,8,00),versus='SM',win=2)
g2=Game(sport=18,date=datetime(2014,12,10,10,00),versus='JE',win=2)

g3=Game(sport=21,date=datetime(2014,12,4,8,00),versus='SM',win=2)
g4=Game(sport=21,date=datetime(2014,12,10,10,00),versus='JE',win=2)

g5=Game(sport=19,date=datetime(2014,12,3,8,00),versus='SM',win=2)
g6=Game(sport=19,date=datetime(2014,12,11,10,00),versus='JE',win=2)

g7=Game(sport=20,date=datetime(2014,12,3,8,00),versus='SM',win=2)
g8=Game(sport=20,date=datetime(2014,12,11,10,00),versus='JE',win=2)

db.session.add(g1)
db.session.add(g2)
db.session.add(g3)
db.session.add(g4)
db.session.add(g5)
db.session.add(g6)
db.session.add(g7)
db.session.add(g8)

db.session.commit()
