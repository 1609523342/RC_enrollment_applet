from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from run import app
from app.forms.error_code import AuthException, TokenException, RootException
from flask import request
from flask import g
from app.models.Application_model import SwitchList, User, SuperUser
from flask import url_for

user_list = ['processing_information', 'personal_information', 'wx_register_root']
admin_list = ['processing_information', 'personal_information', 'change_password', 'wx_register_root']
super_list = ['processing_information', 'personal_information', 'manager_auth', 'change_password', 'wx_register_root']
function_list = [user_list, admin_list, super_list]


# 校验权限
def auth_root(func):
    def analysis_token(*args, **kwargs):
        data = get_token()
        get_login_message(data)
        if func.__name__ in function_list[g.root]:
            return func(*args, **kwargs)
        else:
            raise RootException
    return analysis_token


# 校验网站状态，是否开放登陆
def switch_button(func):
    def check_web_status(*args, **kwargs):
        data = get_token()
        get_login_message()
        button = SwitchList.query.filter(SwitchList.account == 'turn_off_login').first()
        if button:
            if g.root == 2:
                return func(*args, **kwargs)
            elif g.root == 1:
                login_data = get_pass_account(SuperUser)
                if login_data:
                    return func(*args, **kwargs)
                else:
                    url_for()
            elif g.root == 0:
                login_data = get_pass_account(User)
                if login_data:
                    return func(*args, **kwargs)
                else:
                    url_for()
            else:
                raise AuthException(msg='登录失效请重新登录')
        else:
            pass
        return check_web_status


# 获取并解析token
def get_token():
    try:
        token = request.headers['token']
        time = app.config['WX_TIME']
    except Exception as e:
        try:
            token = request.cookies.get('token')
            time = app.config['WEB_TIME']
        except Exception as e:
            raise TokenException(msg='没有获取到token，请重新登录')
    s = Serializer(secret_key=app.config['SECRET_KEY'], expires_in=time)
    try:
        data = s.loads(token.encode('utf-8'))
    except Exception as e:
        raise AuthException(msg='登录失效请重新登录')
    return data


# 将登陆信息赋给g(全局变量)
def get_login_message(data):
    g.root_name = int(data.get('root_name'))
    g.openid = data.get('openid')
    g.root = int(data.get('root'))


# 获取可以登录的账号信息
def get_pass_account(table):
    personal_data = table.query.filter(table.openid == g.openid).first()
    login_data = switch_list.query.filter(switch_list.account == personal_data.account).first()
    return login_data
