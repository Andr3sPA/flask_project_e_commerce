# auth.py
from __future__ import print_function
from flask_login import UserMixin
from __init__ import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    address=db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(150), nullable=True)
    country = db.Column(db.String(150), nullable=True)
    rol=db.Column(db.String(150), nullable=False)
    verificationCode = db.Column(db.String(150), nullable=True)