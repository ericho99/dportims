from app import app
from app.models import *

db.create_all()

g1 = Game(sport=1,date='9/3',versus='JE')
db.session.add(g1)
g2 = Game(sport=1,date='9/7',versus='BR')
db.session.add(g2)
g3 = Game(sport=2,date='9/3',versus='JE')
db.session.add(g3)

p = Player(email='eric.ho@yale.edu')
db.session.add(p)
p2 = Player(email='brian.li@yale.edu')
db.session.add(p2)

a = Attendance(game_id=1,player_id=1)
db.session.add(a)
a2 = Attendance(game_id=1,player_id=2)
db.session.add(a2)
a3 = Attendance(game_id=2,player_id=1)
db.session.add(a3)



db.session.commit()

