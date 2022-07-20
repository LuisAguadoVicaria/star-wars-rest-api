from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

fav_planets = db.Table('fav_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)

fav_characters = db.Table('fav_characters',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    fav_planets = db.relationship('Planets', secondary=fav_planets, lazy='subquery',
        backref=db.backref('users', lazy=True))
    fav_characters = db.relationship('Characters', secondary=fav_characters, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "fav_planets": [x.name for x in self.fav_planets],
            "fav_characters": [x.name for x in self.fav_characters],
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }