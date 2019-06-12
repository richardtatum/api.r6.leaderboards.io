from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db, app
from flask_login import UserMixin
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r6_user = db.Column(db.String(64), index=True)
    avatar = db.Column(db.String(94))

    uplay_data = db.relationship('Data', backref='author', lazy='dynamic')
    weekly_diff = db.relationship('Diff', backref='author', lazy='dynamic')
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_played = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    kd_ratio = db.Column(db.Float(asdecimal=True, decimal_return_scale=2))
    wl_ratio = db.Column(db.Float(asdecimal=True, decimal_return_scale=2))
    waifu = db.Column(db.String(64))
    rank = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Data for: {self.author}>'


class Diff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_played = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    kd_ratio = db.Column(db.Float(asdecimal=True, decimal_return_scale=2))
    wl_ratio = db.Column(db.Float(asdecimal=True, decimal_return_scale=2))

    def __repr__(self):
        return f'<Calculated data for: {self.author}>'


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(4))
    name = db.Column(db.String(64))

    def __repr__(self):
        return f'<Region: {self.ident.upper()}>'


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8))

    def __repr__(self):
        return f'<Platform: {self.name.upper()}>'


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.String(36))
    image = db.Column(db.String(64))
    name = db.Column(db.String(64))
    details = db.Column(db.String(256))

    def __repr__(self):
        return f'<Challenge: {self.name}'