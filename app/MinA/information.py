from . import *
from app.MinA.Authentication import auth_root
from app.forms.error_code import Success, SQLException, SQLMissException, RootException
from ..forms.message_forms import MessageWtforms, PersonalMessageWtforms
from app.models.Application_model import message, User, SuperUser
from flask import request, jsonify, g
from app import db
from run import app
from collections import Iterable


@MinAs.route('/information/', methods=['POST', 'GET', 'DELETE'], endpoint='processing_information')
@auth_root
def processing_information():
    if request.method == 'POST':
        data = request.json
        form = MessageWtforms(data=data)
        form.validate_error_message()
        messages = message()
        messages.set_attrs(form.data)
        try:
            store_processing_data(messages, form)
        except Exception as e:
            raise SQLException()
        return Success()
    elif request.method == 'GET':
        try:
            if g.root == 2:
                data = data_to_dict(message.query.all())
            elif g.root == 1:
                data = data_to_dict(message.query.filter(message.first_choice == g.root_name))
            elif g.root == 0:
                Users = User.query.filter(User.openid == g.openid).first()
                messages = message.query.filter(message.student_id == Users.student_id).order_by(-message.id).first()
                data = data_to_dict(messages)
        except:
            raise SQLMissException()
        return jsonify(data)
    elif request.method == 'DELETE':
        if g.root != 2:
            raise RootException
        else:
            del_id = request.form.get('student_id')
            messages = message.query.filter(message.id == del_id).first()
            db.session.delete(messages)
            db.session.commit()
        return Success(msg='删除成功')


@MinAs.route('/personal/information/', methods=['POST', 'GET'], endpoint='personal_information')
@auth_root
def personal_information():
    if request.method == 'POST':
        data = request.json
        form = PersonalMessageWtforms(data=data)
        form.validate_error_message()
        superusers = SuperUser.query.filter(SuperUser.student_id == form.student_id.data)
        if superusers:
            raise RootException(msg='您无法更改学号和姓名，请先获取邀请码，或者和管理员联系')
        try:
            store_personal_data(form)
        except:
            raise SQLException()
        return Success()
    elif request.method == 'GET':
        try:
            Users = User.query.filter(User.openid == g.openid).first()
        except:
            raise SQLMissException()
        if not Users:
            raise SQLMissException(msg='该条数据不存在')
        return jsonify({'student_id': Users.student_id, 'student_name': Users.student_name})


def store_personal_data(form):
    Users = User.query.filter(User.openid == g.openid).first()
    Users.student_id = form.student_id.data
    Users.student_name = form.student_name.data
    db.session.commit()


def store_processing_data(messages, forms):
    Users = User.query.filter(User.openid == g.openid).first()
    Users.student_id = forms.student_id.data
    Users.student_name = forms.student_name.data
    db.session.add(messages)
    db.session.commit()


def data_to_dict(data):
    data_dict = {}
    Column = print_column()
    if isinstance(data, Iterable):
        for messages in data:
            datas = print_data(messages)
            a = dict(zip(Column, datas))
            data_dict[messages.id] = a
    else:
        datas = print_data(data)
        data_dict = dict(zip(Column, datas))
    return data_dict


def print_data(messages):
    department = app.config['ROOT_AND_DEPARTMENT_NAME']
    datas = [messages.student_id, messages.student_name, messages.sex, messages.birth, messages.grade, messages.major,
             messages.classes, messages.post, messages.other_organization, messages.Speciality, messages.QQ,
             messages.email, messages.phone_number, messages.short_phone, department[int(messages.first_choice)],
             department[int(messages.second_choice)], messages.Personal_profile, messages.Compliance_or_not,
             messages.Ideas_and_creativity, messages.photo_url, messages.Purpose_of_joining, messages.Submission_time]
    return datas


def print_column():
    Column = ['student_id', 'student_name', 'sex', 'birth', 'grade', 'major', 'classes', 'post', 'other_organization',
              'Speciality', 'QQ', 'email', 'phone_number', 'short_phone', 'first_choice', 'second_choice',
              'Personal_profile', 'Compliance_or_not', 'Ideas_and_creativity', 'photo_url', 'Purpose_of_joining',
              'Submission_time']
    return Column