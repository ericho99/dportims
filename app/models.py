from app import db


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
    date = db.Column(db.String(15))
    versus = db.Column(db.String(3))

    def __repr__(self):
        return '#%d: Game: %d date: %s versus: ' % (self.id, self.sport, self.date, self.versus)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

    def __repr__(self):
        return '#%d: Email: %s' % (self.id, self.email)

