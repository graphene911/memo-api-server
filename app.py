from flask import  Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resource.memo import MemoListResource
from config import Config
from resource.user import UserLoginResource, UserLogoutResource, UserRegisterResource, jwt_blacklist



app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)

# JWT Token Library 만들기
jwt = JWTManager(app)

# 로그아웃 된 토큰이 들어있는 set을 jwt에 알려준다.
@jwt.token_in_blocklist_loader
def check_if_otken_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blacklist


api = Api(app)

api.add_resource(MemoListResource, '/memo')
api.add_resource(UserRegisterResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserLogoutResource, '/user/logout')





if __name__ == '__main__' :
    app.run()