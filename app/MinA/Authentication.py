from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from run import app
from app.forms.error_code import AuthException, TokenException, RootException
from flask import request
from flask import g
user_list = ['processing_information', 'personal_information', 'wx_register_root']
admin_list = ['processing_information', 'personal_information', 'change_password', 'wx_register_root']
super_list = ['processing_information', 'personal_information', 'manager_auth', 'change_password', 'wx_register_root']
function_list = [user_list, admin_list, super_list]


def auth_root(func):
    def analysis_token(*args, **kwargs):
        try:
            token = request.headers['token']
            time = app.config['WX_TIME']
        except:
            try:
                token = request.cookies.get('token')
                time = app.config['WEB_TIME']
            except:
                raise TokenException(msg='没有获取到token，请重新登录')
        s = Serializer(secret_key=app.config['SECRET_KEY'], expires_in=time)
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            raise AuthException(msg='登录失效请重新登录')
        g.root_name = int(data.get('root_name'))
        g.openid = data.get('openid')
        g.root = int(data.get('root'))
        if func.__name__ in function_list[g.root]:
            return func(*args, **kwargs)
        else:
            raise RootException
    return analysis_token
