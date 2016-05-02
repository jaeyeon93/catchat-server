# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

users = {
    'user1' : {'name' : 'user1', 'id' : 'user1_id','email' : 'user1@naver.com', 'password' : 'user1password' },
    'user2' : {'name' : 'user2', 'id' : '2_id','email' : 'user2email@daum.com', 'password' : '2password' },
    'user3' : {'name' : 'user3', 'id' : 'user3_id','email' : 'user3@naver.com', 'password' : '3password' },
    'user4' : {'name' : 'user4', 'id' : '4_id','email' : 'user4@.com', 'password' : 'user4password' }
}

def user_not_exist(user_id):
    if user_id not in users:
        abort(404, message="user {} does not exist".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('id')
parser.add_argument('email')
parser.add_argument('password')
# only user side not add userlist
class user(Resource):
    def get(self, user_id):
        user_not_exist(user_id)
        return users(user_id)

    def delete(self, user_id):
        user_not_exist(user_id)
        del users[user_id]
        return '', 200
    def put(self, user_id):
        user_not_exist(user_id)
        args = parser.parse_args()

        user_upload = {}
        user_upload['name'] = args['name']
        user_upload['id'] = args['id']
        user_upload['email'] = args['email']
        user_upload['password'] = args['password']

        users[user_id] = user_upload
        return user_id, 200


api.add_resource(user, '/api/v1/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)