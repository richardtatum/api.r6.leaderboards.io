from app import api
from flask_restful import Resource, reqparse, abort
from app.models import User, Data, Diff, Challenge
import os

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Only accepts valid site user IDs.')
parser.add_argument('authorization', type=str)
parser.add_argument('challenges', help='Currently Weekly Challenges')


def abort_user_search(user_id):
    if not User.query.filter_by(r6_user=user_id).first():
        abort(404, message=f'User with name {user_id} does not exist')


def auth_required(auth):
    if auth != os.environ['API_AUTH']:
        abort(401, message='Unauthorized.')


class UserSearch(Resource):
    def get(self):
        args = parser.parse_args()
        abort_user_search(args['username'])
        auth_required(args['authorization'])
        u = User.query.filter_by(r6_user=args['username']).first()
        d = Data.query.filter_by(author=u).first()
        w = Diff.query.filter_by(author=u).first()
        return {
            'Username': u.r6_user,
            'Platform': u.platform.name,
            'Region': u.region.name,
            'Overall': {
                    'Time Played': d.time_played,
                    'Kills': d.kills,
                    'Deaths': d.deaths,
                    'K/D Ratio': float(d.kd_ratio),
                    'W/L Ratio': float(d.wl_ratio),
                    'Waifu': d.waifu,
                },
            'Weekly': {
                    'Time Played': w.time_played,
                    'Kills': w.kills,
                    'Deaths': w.deaths,
                    'K/D Ratio': float(w.kd_ratio),
                    'W/L Ratio': float(w.wl_ratio),
                },
            'profile': u.avatar,
            'waifu_img': f'https://cdn.r6.leaderboards.io/images/operator_images/{d.waifu}.png'
            }, 200


class Challenges(Resource):
    def get(self):
        args = parser.parse_args()
        auth_required(args['authorization'])
        output = {}
        for c in Challenge.query.all():
            output[c.name] = c.details
        return output, 200


api.add_resource(UserSearch, '/user')
api.add_resource(Challenges, '/weekly_challenge')