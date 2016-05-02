# -*- coding: utf-8 -*-
from flask import Flask
# flask module에서 Flask모듈을 삽입? 임포트
from flask_restful import reqparse, abort, Api, Resource
# flask_restful모듈에서 reqparse, abort, Api, Resource라는 모듈을 삽입
app = Flask(__name__)
# app instance를 생성, app(flask.Flask)
api = Api(app)
# api instance생성
# Api는 class flask_restful.Api이다.

USERS = {
    'user1' : {'email': 'hello@naver.com', 'password' : '1234'},
    'user2' : {'email': 'world@naver.com', 'password': '5678'},
    'user3' : {'email': 'jaeyeon@naver.com', 'password': '12345'}
}
# USERS라는 딕셔너리를 생성을 하고, key값으로 user1,user2,user3...을 주고, value값으로 새로운 딕셔너리를 생성. 새로운 딕셔너리의 key값은 email, password이다.

def user_not_exist(user_id):
    # user_not_exist라는 함수를 생성. 파라미터는 user_id값을 받는다.
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))
        # abort함수는 http예외를 주어진 http-protocol값으로 일부러 오류를 발생시키는거다.
        # 만약에 USERS에 user_id가 없으면 404 http오류를 발생시킨다. 그리고 user <user_id> doesn't exist라는 메세지를 띄운다.

parser = reqparse.RequestParser()
# parser는 reqparse클래스에서 RequestParse라는 함수를 호출한 객체?인스턴스?
parser.add_argument('email')
# 'email'이라는 인수를 추가한다.
parser.add_argument('password')
# password라는 인수를 추가한다.

class User(Resource):
    # User Class인데 이부분은 User전체가 아닌 user_id 개개인적인 부분에 대해서 작동. 전체가 아닌 하나에대해서 get, delete, put을 한다.
    # User class에 Resource를 상속했다. Resource는 추상적인 RESTful resource를 대표한다.?
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
        # put method로서, 전달받은 user_id한 args를 업로드를 하는 역할
        args = parser.parse_args()
        # parse.parse_args()는 요청된 응답에 대해서,모든 인수를 분석 그리고 결과값으로 namespace를 리턴해준다.
        user_not_exist(user_id)
        # user_not_exist함수에서 user_id가 없으면 404 protocol을 리턴, 있으면 그냥 페스

        a = {}
        # a라는 빈 딕셔너리를 생성
        a["email"] = args['email']
        # a딕셔너리의 key값으로 'email'을 추가하고 value값으로 전달받은? 입력한 인수를 대입한다.
        a["password"] = args['password']
        # a딕셔너리의 key값으로 password를 추가하고 value값으로 입력받은 password인수를 대입

        USERS[user_id] = a
        # a 딕셔너리의 값들을 USERS딕셔너리의 호출한 user_id의 key값과 value값으로 대입
        # put method는 업로드를 시키는건데, 기존의 있던 부분들을 업로드? 바꿔치기를 해야된다.
        # a = {}라는 빈 딕셔너리를 생성을 하고, 그 안에 email(key값)은 args['email']이라는 value값을 업로드, password(key값)은 args['password']로 업로드한다.
        return a, 200
        # 딕셔너리 a를 대입하고 http protocol 200을 리턴.
class UserList(Resource):
    # UserList를 보는 class, class Resource를 상속한다.
    def get(self):
        return USERS
    # get method를 받으면 users 전체 리스트를 리턴해준다.
    def post(self):
        # post method를 호출.
        args = parser.parse_args()
        # class parser에 있는 parse_args()함수를 호출을 해서, 요청된 응답에 대해서 모든 인수들을 분석하고, 결과값을 args에 리턴해준다.
        user_id = int(max(USERS.keys()).lstrip('user')) + 1
        # USERS.keys()는 USERS딕셔너리의 key값들을 모아서 dict_keys라는 객체를 리턴한다.
        # USERS 딕셔너리의 key값들은 user1, user2, user3 ... 으로 user들의 숫자가 붙은 값이다.
        # max(USERS.keys())는 리턴받은 리스트중에서 가장큰(가장나중?)에 있는 요소를 리턴을 해준다. 예를 들어 user5까지 있다면 user5를 리턴.
        # lstrip('')은 ''사이에 있는 문자열을 제거를 해주는 역할이다. max(USERS.keys()).lstrip('user')는 user5를 리턴받았을때 user라는 문자열부분을 제거하라는 뜻.
        # user5에서 user문자열을 제거를 하면 5가 남지만, 5는 문자열이기때문에 앞에 int('5')를 통해 문자열 5를 정수형 5로 바꿔준다.
        # 정수형 5가 리턴이 되고 거기에 +1을 더해서 정수형 6을 만든다. 정수형 6을 user_id에 대입한다.
        user_id = 'user%i' % user_id
        # 이전줄의 user_id는 정수6이다. 'user%i' % user_id에서 i자리에 user_id값을 입력받으니 'user6'이다. 이것을 다시 user_id에 대입한다.
        # 여기 i를 처음에 number로 했다가 문제가 됬다.
        USERS[user_id] = {'email': args['email'], 'password' : args['password']}
        # 딕셔너리 USERS의 key값 user_id는 value로 딕셔너리를 받고, value의 key값은 'email', 'password'다.
        a = {}
        # a 라는 빈 딕셔너리를 생성
        a['email'] = args['email']
        # a의 key값은 'email'이고 value는 입력받은 email값이다.
        a['password'] = args['password']
        # a의 key값은 password이고 입력받은 password가 value값이다. 입력받은 value값을 a딕셔너리의 'password' key의 value로 대입
        USERS[user_id] = a
        # USERS['user6'] 딕셔너리의 value값은 a 딕셔너리이다.
        return a, 200
        # a 딕셔너리를 리턴해주고, http 200을 리턴해준다.


api.add_resource(UserList, 'api/v1/Users')
# add_resource는 api에 resource를 추가를 하는것이다. UserList를 추가하고, localhost:5000/api/vi/Users라는 라우트를 살정
api.add_resource(User, '/api/v1/users/<user_id>')
# User resouce를 추가하고, /api/v1/users/<user_id>라는 라우트를 설정

if __name__ == '__main__':
    app.run(debug=True)
    #if__name__ == '__main__'은 직접 이 파일을 실행시켰을때 실행이 되고, 외부에서 이 파일(모듈)을 불러서 사용할 때는 거짓이 된다.
