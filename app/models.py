from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15))
    name = db.Column(db.String(26))
    admin = db.Column(db.Integer)
    blocked = db.Column(db.Integer)
    panlist_id = db.Column(db.Integer, db.ForeignKey('panlists.id'))
    # panlist = db.relationship('Panlist', backref="users")

    def __repr__(self):
        return '#%d: name: %s number: %s panlist id: %d isAdmin: %d blocked: %d' % (self.id, self.name, self.number, self.panlist_id, self.admin, self.blocked)

class Panlist(db.Model):
    __tablename__ = 'panlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '#%d: Panlist %s ' % (self.id, self.name)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    versus = db.Column(db.String(7))
    win = db.Column(db.Integer) #0 for a loss, 1 for a win, 2 if the game has yet to be played, 3 for a tie

    def __repr__(self):
        return '#%d: Game: %d date: %s versus: %s win: %d' % (self.id, self.sport, self.date, self.versus, self.win)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(10))
    name = db.Column(db.String(25))
    email = db.Column(db.String(50))

    def __repr__(self):
        return '#%d: Netid: %s Name: %s Email: %s' % (self.id, self.netid, self.name, self.email)

class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))

    def __repr__(self):
        return '#%d: game_id: %d player_id: %d' % (self.id, self.game_id, self.player_id)




