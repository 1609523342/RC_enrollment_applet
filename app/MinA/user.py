from collections import Iterable
from . import *
import requests
from run import app
from app.models.Application_model import User, SuperUser
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import jsonify, request, g
from app.forms.message_forms import WebLoginWtforms, CreatAdminWtforms, WeiXinRegisterRootWtform, ChangePasswordWtform
from app.forms.error_code import LoginException, Success, SQLException, SQLMissException, RootException
from flask import make_response
from app.MinA.Authentication import auth_root

@MinAs.route('/wxUser/', methods=['POST'])#clear
def user_wx_login():
    Api = app.config['WX_LOGIN_API']
    response = requests.get(Api)
    user_data = response.json()
    openid = user_data['openid']
    sql_data = User.query.filter(User.openid == openid).first()
    if sql_data is None:
        token_context = wx_token_message(creat_and_save_sqldata(openid))
    else:
        token_context = wx_token_message(sql_data)
    return jsonify(creat_token(token_context))


@MinAs.route('/webUser/', methods=['POST'])#clear
def User_web_login():
    form = WebLoginWtforms(request.form)
    form.validate_error_message()
    superusers = SuperUser.query.filter(SuperUser.account == form.account.data).first()
    if superusers and superusers.check_password(form.password.data):
        token = creat_token(web_token_message(superusers), time=app.config['WEB_TIME'])
        response = set_cookies(token)
        return response
    elif superusers is None:
        return LoginException(msg='查询不到该账户，请找裕虎质问其是否偷懒')
    else:
        return LoginException(msg='密码不正确，请重新输入')


@MinAs.route('/admin/', methods=['POST', 'GET', 'DELETE'])#clear
@auth_root
def manager_auth():
    if request.method == 'POST':
        form = CreatAdminWtforms(request.form)
        form.validate_error_message()
        superuers = SuperUser()
        superuers.set_attrs(form.data)
        if SuperUser.query.filter(SuperUser.student_id == superuers.student_id).first() is None:
            try:
                db.session.add(superuers)
                db.session.commit()
            except:
                SQLException(msg='无法写入数据库')
        else:
            raise SQLException(msg='此账号已存在，创建失败')
        return Success(msg='账号创建成功')
    elif request.method == 'GET':
        try:
            superuser = SuperUser.query.all()
        except:
            raise SQLMissException
        return jsonify(show_root_message(superuser))
    elif request.method == 'DELETE':
        del_id = request.form.get('student_id')
        superuser = SuperUser.query.filter(SuperUser.student_id == del_id).first()
        if superuser is None:
            raise SQLMissException(msg='数据库不存在该条数据')
        users = User.query.filter(User.student_id == del_id).first()
        if users:
            users.root = '0'
            users.root_name = '7'
            db.session.commit()
        try:
            db.session.delete(superuser)
            db.session.commit()
        except:
            raise SQLException(msg='数据无法删除')
        return Success(msg='删除成功')


@MinAs.route('/password/', methods=['POST'], endpoint='password')#clear
@auth_root
def change_password():
    form = ChangePasswordWtform(request.form)
    form.validate_error_message()
    superusers = SuperUser.query.filter(SuperUser.student_id == g.openid).first()
    if superusers and superusers.check_password(form.password.data):
        try:
            superusers.password = form.password1.data
            db.session.commit()
        except:
            raise SQLException()
        return Success(msg='密码修改成功')
    elif superusers.check_password(form.password.data) == False:
        return RootException(msg='密码错误，修改失败')
    else:
        return SQLMissException(msg='无此账号信息，请检查是否输入有误')


@MinAs.route('/wxadmin/', methods=['POST', 'GET'], endpoint='wxadmin')#clear
@auth_root
def wx_register_root():
    if request.method == 'POST':
        form = WeiXinRegisterRootWtform(request.form)
        form.validate_error_message()
        superusers = SuperUser.query.filter(SuperUser.student_id == form.student_id.data).first()
        if superusers and superusers.check_password(form.password.data):
            users = User.query.filter(User.openid == g.openid).first()
            users.root = superusers.root
            users.root_name = superusers.root_name
            superusers.student_name = users.student_name = form.student_name.data
            users.student_id = form.student_id.data
            db.session.commit()
            return Success(msg='权限提升成功')
        elif superusers is None:
            return SQLMissException(msg='您没有被邀请，请联系管理员解决')
        elif superusers.check_password(form.password.data) == False:
            return RootException(msg='邀请码错误')
    if request.method == 'GET':
        users = User.query.filter(User.openid == g.openid).first()
        return jsonify(show_root_message(users))



def creat_token(token_context, time=app.config['WX_TIME']):
    s = Serializer(secret_key=app.config['SECRET_KEY'], expires_in=time)
    token = s.dumps(token_context).decode('utf-8')
    return token


def creat_and_save_sqldata(openid):
    User_login = User(openid=openid, root='0', root_name='7',
                      student_id='无', student_name='无')
    db.session.add(User_login)
    db.session.commit()
    return User_login


def wx_token_message(sql_data):
    token_dict = {'openid': sql_data.openid, 'root': sql_data.root,
                  'root_name': sql_data.root_name}
    return token_dict


def web_token_message(sql_data):
    token_dict = {
        'openid': sql_data.student_id,
        'root': sql_data.root,
        'root_name': sql_data.root_name
    }
    return token_dict


def set_cookies(token):
    header = {'Content-Type': 'application/json'}
    response = make_response('登录成功', header)
    response.set_cookie('token', token)
    return response


def show_root_message(Superuser):
    department = app.config['ROOT_AND_DEPARTMENT_NAME']
    root = app.config['ROOT']
    data_dict = {}
    Column = ['student_id', 'student_name', 'root', 'root_name']
    if isinstance(Superuser, Iterable):
        for superuser in Superuser:
            superusers = [superuser.student_id, superuser.student_name, root[int(superuser.root)],
                          department[int(superuser.root_name)]]
            a = dict(zip(Column, superusers))
            data_dict[superuser.id] = a
    else:
        datas = [Superuser.student_id, Superuser.student_name,root[int(Superuser.root)],
                 department[int(Superuser.root_name)]]
        data_dict = dict(zip(Column, datas))
    return data_dict


