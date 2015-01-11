from app import app
from app.models import *
from datetime import datetime

g1 = Game(sport=10,date=datetime(2014,1,16,3,15),versus='ALL',win=2)
g2 = Game(sport=10,date=datetime(2014,1,23,3,15),versus='ALL',win=2)
g3 = Game(sport=10,date=datetime(2014,1,30,3,15),versus='ALL',win=2)
g4 = Game(sport=10,date=datetime(2014,2,6,3,15),versus='ALL',win=2)
g5 = Game(sport=10,date=datetime(2014,2,13,3,15),versus='ALL',win=2)
g6 = Game(sport=10,date=datetime(2014,2,20,3,15),versus='ALL',win=2)

g7 = Game(sport=13,date=datetime(2014,1,13,9,15),versus='JE',win=2)
g8 = Game(sport=13,date=datetime(2014,1,29,8,30),versus='BR',win=2)
g9 = Game(sport=13,date=datetime(2014,2,3,11,15),versus='MC',win=2)
g10 = Game(sport=13,date=datetime(2014,2,5,9,30),versus='PC',win=2)
g11 = Game(sport=13,date=datetime(2014,2,12,8,30),versus='ES',win=2)

db.session.add(g1)
db.session.add(g2)
db.session.add(g3)
db.session.add(g4)
db.session.add(g5)
db.session.add(g6)
db.session.add(g7)
db.session.add(g8)
db.session.add(g9)
db.session.add(g10)
db.session.add(g11)
