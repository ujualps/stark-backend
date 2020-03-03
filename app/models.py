from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    email = db.Column(db.String(50))
    Designation = db.Column(db.String(50))
    DOB = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))