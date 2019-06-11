from app import app, db, api
from flask_restful import Resource, reqparse, abort
from app.models import User
from settings import stats_choices

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='Only accepts valid site user IDs.')
parser.add_argument('stats', type=str, choices=stats_choices, help='Requestable stats available at web.site.')

# u = User.query.get(21)

def abort_user_search(user_id):
    if not User.query.get(user_id):
        abort(404, message=f'User with ID {user_id} does not exist')


class UserSearch(Resource):
    def get(self):
        args = parser.parse_args()
        abort_user_search(args['id'])
        u = User.query.get(args['id'])
        stat = args['stats']
        return {'hello': u.r6_user,
                'stats': stat}, 200, {'stats': stat}

api.add_resource(UserSearch, '/user')