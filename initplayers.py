from app import app
from app.models import *
from datetime import datetime

db.drop_all()
db.create_all()

g1 = Game(sport=1,date=datetime(2014,9,03,5,05),versus='JE',win=0)
db.session.add(g1)
g2 = Game(sport=1,date=datetime(2014,9,07,3,50),versus='BR',win=2)
db.session.add(g2)
g3 = Game(sport=2,date=datetime(2014,9,3,5,00),versus='JE',win=2)
db.session.add(g3)
g4 = Game(sport=1,date=datetime(2014,9,01,3,50),versus='BK',win=1)
db.session.add(g4)

p = Player(netid='eh425',name='Eric Ho',email='eric.ho@yale.edu')
db.session.add(p)
p2 = Player(netid='bl123',name='Brian Li',email='brian.li@yale.edu')
db.session.add(p2)

a = Attendance(game_id=1,player_id=1)
db.session.add(a)
a2 = Attendance(game_id=1,player_id=2)
db.session.add(a2)
a3 = Attendance(game_id=2,player_id=1)
db.session.add(a3)



db.session.commit()

