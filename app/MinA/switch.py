from collections import Iterable

from . import *
from flask import request, jsonify
from app import db
from app.models.Application_model import SwitchList, SuperUser
from app.forms.error_code import Success, SQLMissException, SQLException, LoginException
from app.forms.message_forms import AccessAccount


"""
后台开关，开启之后默认只有超管权限可以访问，即‘2’权限
开关实现思路：新建立一张数据表，往表中写入’turnofflogin‘
登录的时候会先检测该表是否存在该条数据，若存在则限制登录，不存在则不限制登录
"""


@MinAs.route('/switch/', endpoint='on', methods=['DELETE', 'POST'])
def turn_on_switch():
    # 开放登录
    if request.method == 'DELETE':
        # 查询表中是否有该标记
        button = SwitchList.query.filter(SwitchList.account == 'turnofflogin').first()
        # 有则删掉，开放登陆
        if button:
            db.session.delete(button)
            return Success(msg='网站开放登陆成功')
        else:
            return Success(msg='网站已经开放登陆，无需再次开放')
    # 关闭开放
    elif request.method == 'POST':
        try:
            # 查询出表中所有数据
            account = SwitchList.query.all()
        except Exception as e:
            raise SQLMissException
        try:
            # 将标记添加到表中，并把之前的加进去可以访问的账号通通删除
            button = SwitchList(account='turn_off_login')
            db.session.delete(account)
            db.session.commit()
            db.session.add(button)
            db.session.commit()
        except Exception as e:
            raise SQLException(msg='限制登录失败，无法访问数据库')
        return Success(msg='限制登录开启成功')
    else:
        raise LoginException('请求有误，拒绝访问')

"""
对于访问后台的人员的控制功能
支持一键导入超管和普通管理员开放其登陆后台
支持单独增删账号来控制登陆
"""
@MinAs.route('/AccessList/', endpoint='off', methods=['GET', 'POST', 'DELETE', 'PUT'])
def access_list():
    # 一键导入所有超管和普通管理员账号，实现管理员的开放登陆
    if request.method == 'PUT':
        try:
            superuser = SuperUser.query.all()
        except Exception as e:
            raise SQLMissException(msg='查询不到对应数据，请检查数据库连接')
            # 获取超管和普通管理员的账号导入到可登录名单的表中
            get_and_add_account(superuser)
            return Success(msg='普通管理员登录开启')
    # 单独添加人员访问后台
    elif request.method == 'POST':
        # 传入的账号格式验证：满足12个字符串（即学号的长度）。
        # 数据从body的form-data中获取获取数据
        data = AccessAccount(data=request.form)
        data.validate_error_message()
        account = SwitchList(account=data.account)
        try:
            # 添加到数据库中
            db.session.add(account)
            db.session.commit()
        except Exception as e:
            raise SQLException(msg='数据无法上传，请检查数据库连接')
    # 获取登录人员
    elif request.method == 'GET':
        try:
            account_list = SwitchList.query.all()
        except Exception as e:
            raise SQLMissException(msg='查询不到数据，请检查数据库连接')
        account_list_data = print_account_list(account_list)
        return jsonify(account_list_data)
    elif request.method == 'DELETE':
        try:
            data = SwitchList.query.filter(SwitchList.account == request.form.get('account')).first()
        except Exception as e:
            raise SQLMissException(msg='获取数据失败，请检查数据库连接')
        try:
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            raise SQLException(msg='数据更新失败，请检查数据库连接')


def get_and_add_account(superuser):
    try:
        for admin in superuser:
            admin_list = SwitchList(account=admin.account)
            db.session.add(admin_list)
    except Exception as e:
        raise SQLException(msg='账号写入失败，请检查数据库连接')


def print_account_list(switch_list):
    account_dict = {}
    if isinstance(switch_list, Iterable):
        for account in switch_list:
            account_dict[account.id] = account.account
        return account_dict
    else:
        return {SwitchList.id: SwitchList.account}
