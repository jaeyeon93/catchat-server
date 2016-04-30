from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

USERS = {
    'user1' : {'email': 'hello@naver.com', 'password' : '1234'},
    'user2' : {'email': 'world@naver.com', 'password': '5678'},
    'user3' : {'email': 'jaeyeon@naver.com', 'password': '12345'}
}

def user_not_exist(user_id):
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

class User(Resource):
    def get(self, user_id):
        user_not_exist(user_id)
        print 'hello'
        return USERS[user_id]

    def delete(self, user_id):
        user_not_exist(user_id)
        del USERS[user_id]
        return '', 200

    def put(self, user_id):
        args = parser.parse_args()
        user_not_exist(user_id)

        a = {}
        a["email"] = args['email']
        a["password"] = args['password']

        USERS[user_id] = a

class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        user_id = int(max(USERS.keys()).lstrip('user')) + 1


api.add_resource(User, '/api/v1/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
