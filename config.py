import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database settings
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_HOST = os.environ['DB_HOST']
    DB_NAME = os.environ['DB_NAME']

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 170
    SQLALCHEMY_POOL_TIMEOUT = 120


rank_list = {
    '20': 'Diamond', '19': 'Platinum I',
    '18': 'Platinum II', '17': 'Platinum III',
    '16': 'Gold I', '15': 'Gold II',
    '14': 'Gold III', '13': 'Gold IV',
    '12': 'Silver I', '11': 'Silver II',
    '10': 'Silver III', '9': 'Silver IV',
    '8': 'Bronze I', '7': 'Bronze II',
    '6': 'Bronze III', '5': 'Bronze IV',
    '4': 'Copper I', '3': 'Copper II',
    '2': 'Copper III', '1': 'Copper IV',
    '0': 'Not Ranked Yet'
        }


def time_format(s):
    """ Takes seconds data and formats it into
        days, hours, minutes and seconds """
    minutes, seconds = divmod(s, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if s < 3600:
        return f'{minutes}m'
    elif s < 86400:
        return f'{hours}h {minutes}m'
    else:
        return f'{days}d {hours}h {minutes}m'