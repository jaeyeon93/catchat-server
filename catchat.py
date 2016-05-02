# -*- coding: utf-8 -*-
from flask import Flask
# flask module에서 Flask모듈을 삽입? 임포트
from flask_restful import reqparse, abort, Api, Resource
# flask_restful모듈에서 reqparse, abort, Api, Resource라는 모듈을 삽입
app = Flask(__name__)
api = Api(app)
# 심플코드 연습용

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
    # User Class인데 이부분은 User전체가 아닌 user_id 개개인적인 부분에 대해서 작동. 전체가 아닌 하나에대해서 get, delete, put을 한다.
    def get(self, user_id):
        user_not_exist(user_id)
        return USERS[user_id]
    # get method로서 user_id가 있으면 USERS 딕셔너리에서 호출한 user_id(key값)에 대한 value를 리턴한다.
    def delete(self, user_id):
        user_not_exist(user_id)
        del USERS[user_id]
        return '', 200
    # delete method로서 user_id(key값)을 보내면 해당값에 대해서 ''(공백)을 리턴함으로써 삭제를 한다. 그리고 http protocol 200을 보내는데 이것은 오류없이 성공했다는 의미
    def put(self, user_id):
        args = parser.parse_args()
        user_not_exist(user_id)

        a = {}
        a["email"] = args['email']
        a["password"] = args['password']
        # put method는 업로드를 시키는건데, 기존의 있던 부분들을 업로드? 바꿔치기를 해야된다.
        # a = {}라는 빈 딕셔너리를 생성을 하고, 그 안에 email(key값)은 args['email']이라는 value값을 업로드, password(key값)은 args['password']로 업로드한다.
        USERS[user_id] = a
        return a, 200

class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        user_id = int(max(USERS.keys()).lstrip('user')) + 1
        user_id = 'user%i' % user_id
        # 여기 i를 처음에 number로 했다가 문제가 됬다.
        USERS[user_id] = {'email': args['email'], 'password' : args['password']}
        a = {}
        a['email'] = args['email']
        a['password'] = args['password']
        USERS[user_id] = a
        return a, 200


api.add_resource(UserList, 'api/v1/Users')
api.add_resource(User, '/api/v1/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
    #if__name__ == '__main__'은 직접 이 파일을 실행시켰을때 실행이 되고, 외부에서 이 파일(모듈)을 불러서 사용할 때는 거짓이 된다.
