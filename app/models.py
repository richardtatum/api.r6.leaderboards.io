from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db, app
from flask_login import UserMixin
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r6_user = db.Column(db.String(64), index=True)
    ubi_id = db.Column(db.String(64), index=True)
    plat_id = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(94))

    uplay_data = db.relationship('Data', backref='author', lazy='dynamic')
    weekly_data = db.relationship('Weekly', backref='author', lazy='dynamic')
    weekly_diff = db.relationship('Diff', backref='author', lazy='dynamic')
    op_data = db.relationship('OperatorData', backref='author', lazy='dynamic')
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    gifs = db.relationship('Gif', backref='author', lazy='dynamic')
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))

    twitch = db.Column(db.String(80), nullable=True)
    youtube = db.Column(db.String(80), nullable=True)
    mixer = db.Column(db.String(80), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.r6_user}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=86400):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def join_clan(self, clan_id):
        self.clan = clan_id

    def leave_clan(self):
        self.clan = None

    def is_admin(self):
        if self.clan:
            return self.id == self.clan.clan_admin
        else:
            return False

    def set_region(self, region_id):
        self.region = region_id


class Clan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clan_name = db.Column(db.String(128), index=True, unique=True)
    clan_avatar = db.Column(db.String(128))
    clan_admin = db.Column(db.Integer, index=True, unique=True)
    users = db.relationship('User', backref='clan', lazy='dynamic')

    def set_admin(self, user):
        self.clan_admin = user.id

    def set_avatar(self, clan_name):
        self.clan_avatar = f'{tiny}{clan_name.replace(" ", "%20")}{graphs}'

    def delete_clan(self):
        for u in self.users:
            u.leave_clan()

    def __repr__(self):
        return f'<Clan: {self.clan_name}>'


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


class Weekly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_played = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Weekly data for: {self.author}>'


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


class OperatorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(5))
    roundwon = db.Column(db.Integer)
    roundlost = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    death = db.Column(db.Integer)
    timeplayed = db.Column(db.Integer)
    gadget = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Operator {index} data for <{self.author}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(1600))
    created = db.Column(db.DateTime)

    def __repr__(self):
        return f'Ticket created: {self.created}'

    def is_valid(self):
        # Checks if creation date is older than ~2.7 hours
        if self.created < datetime.now() - timedelta(seconds=10000):
            return False
        else:
            return True


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(4))
    name = db.Column(db.String(64))
    users = db.relationship('User', backref='region', lazy='dynamic')

    def __repr__(self):
        return f'<Region: {self.ident.upper()}>'


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(8))
    name = db.Column(db.String(8))
    users = db.relationship('User', backref='platform', lazy='dynamic')

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


class Gif(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frame = db.Column(db.String(256))
    mp4 = db.Column(db.String(256))
    webm = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Gif {self.id} for: {self.author}.>'


class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, unique=False, default=False)
    message = db.Column(db.String(256))

    def __repr__(self):
        return f'<Maintenance message>'


class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(5))
    name = db.Column(db.String(64))
    gadget = db.Column(db.String(64))

    def __repr__(self):
        return f'<Operator {self.name} {self.index}>'

