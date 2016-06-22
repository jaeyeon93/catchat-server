# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/alchemy_new'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

user_inf = {'user1' : {'username':'jaeyeonkim','email':'jaeyeon93@naver.com', 'password':'12345'}}

def not_exist(user_id):
    if user_id not in user_inf:
        abort(404, message="{} does not exist".format(user_id))
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('email')
parser.add_argument('password')

class user(Resource):
    def get(self, user_id):
        not_exist(user_id)
        return user_inf[user_id]
    def delete(self,user_id):
        not_exist(user_id)
        del user_inf[user_id]
        return '', 200
    def put(self,user_id):
        args = parser.parse_args()
        not_exist(user_id)

        a = {}
        a['username'] = args['username']
        a['email'] = args['email']
        a['password'] = args['password']

        user_inf[user_id] = a
        return a, 200
class userlist(Resource):

    def get(self):
        return user_inf
    def post(self):
        args = parser.parse_args()
        # user_id = int(max(user_inf.keys()).lstrip('user')) + 1
        # user_id = 'user%i' % user_id

        new_user = user_inf(args['username'], args['email'], args['password'])
        new_user_id = db.session.add(new_user)
        db.session.commit()
        return new_user_id, 200

api.add_resource(userlist, '/users')
api.add_resource(user,'/api/v1/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)