from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15))
    panlist_id = db.Column(db.Integer, db.ForeignKey('panlists.id'))
    panlist = db.relationship('Panlist', backref="users")

    def __repr__(self):
        return '#%d: number: %s' % (self.id, self.number)

class Panlist(db.Model):
    __tablename__ = 'panlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '#%d: Panlist %s ' % (self.id, self.name)
