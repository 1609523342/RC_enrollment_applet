from wtforms import Form, StringField, IntegerField,validators
from wtforms.validators import length, email, DataRequired, NumberRange, EqualTo
from app.forms.base_forms import BaseForm
from time import asctime
from run import app


class MessageWtforms(BaseForm):
    student_id = StringField(validators=[DataRequired(message='学号不能为空'), length(12, message='学号长度不正确')])
    student_name = StringField(validators=[DataRequired(message='名字不能为空'), length(max=16, message='姓名字段大于最大长度')])
    sex = StringField(validators=[DataRequired(message='性别不能为空'), length(max=4, message='性别字段大于最大长度')])
    birth = StringField(validators=[DataRequired(message='生日不能为空'), length(max=16, message='出生年月日字段大于最大长度')])
    grade = IntegerField(validators=[DataRequired(message='年级不能为空'), length(max=32, message='年级字段大于最大长度')])
    major = StringField(validators=[DataRequired(message='专业不能为空'), length(max=32, message='专业字段大于最大长度')])
    classes = StringField(validators=[DataRequired(message='班级不能为空'), length(max=16, message='班级字段大于最大长度')])
    post = StringField(validators=[DataRequired(message='曾任职务不能为空，没有则填无'), length(max=16, message='曾任职务字段大于最大长度')], default='无')
    other_organization = StringField(validators=[DataRequired(message='加入的其他组织或社团不能为空，没有则填无'), length(max=64, message='其他组织字段大于最大长度')])
    Speciality = StringField(validators=[DataRequired(message='爱好不能为空'), length(max=64, message='特长字段大于最大长度')])
    QQ = StringField(validators=[length(min=7, max=11, message='QQ不符合长度要求')], default=0)
    email = StringField(validators=[email(message='请输入正确的邮箱')])
    phone_number = StringField(validators=[length(11, message='手机号码不符合要求')])
    short_phone = StringField(validators=[DataRequired(message='短号不能为空，没有则填无')])
    first_choice = StringField(validators=[DataRequired(message='第一志愿不能为空'), NumberRange(min=1, max=6, message='第一志愿输入有误')])
    second_choice = StringField(validators=[DataRequired(message='第二志愿不能为空'), NumberRange(min=1, max=6, message='第二志愿输入有误')])
    Compliance_or_not = StringField(validators=[DataRequired(message='是否服从分配不能为空'), length(max=16, message='字段超过最大长度')])
    Personal_profile = StringField(validators=[DataRequired(message='个人简介不能为空'), length(max=256, message='字段超过最大长度')])
    photo_url = StringField(default='无')
    Ideas_and_creativity = StringField(validators=[DataRequired(message='创意和想法不能为空'), length(max=256, message='字段超过最大长度')])
    Purpose_of_joining = StringField(validators=[DataRequired(message='加入原因不能为空'), length(max=256, message='字段超过最大长度')])
    Submission_time = StringField(validators=[DataRequired(message='提交时间出错，请联系管理员')], default=asctime())


class PersonalMessageWtforms(BaseForm):
    student_id = StringField(validators=[DataRequired(message='字段不能为空'), length(12, message='学号长度不正确')])
    student_name = StringField(validators=[DataRequired(message='字段不能为空'), length(max=16, message='姓名字段大于最大长度')])


class WebLoginWtforms(BaseForm):
    account = StringField(validators=[DataRequired(message='字段不能为空'), length(12, message='账号格式错误')])
    password = StringField(validators=[DataRequired(message='密码不能为空')])


class CreatAdminWtforms(BaseForm):
    student_id = StringField(validators=[DataRequired(message='学号不能为空'), length(12, message='学号长度不正确')])
    root = StringField(validators=[DataRequired(message='权限不能为空')])
    root_name = StringField(validators=[DataRequired(message='部门名称不能为空')])
    account = StringField(validators=[DataRequired(message='账号不能为空'), length(min=10, max=20, message='账号长度在10~20之间请检查长度是否符合要求')])
    password = StringField(default=app.config['INVITATION_CODE'], validators=[DataRequired(message='邀请码不能为空'), length(max=16, message='邀请码大于最大长度')])
    student_name = StringField(default='无')


class WeiXinRegisterRootWtform(BaseForm):
    student_id = StringField(validators=[DataRequired(message='学号不能为空'), length(12, message='学号长度不正确')])
    student_name = StringField(validators=[DataRequired(message='学号不能为空'), length(max=16, message='姓名字段大于最大长度')])
    password = StringField(validators=[DataRequired(message='邀请码不能为空')])


class ChangePasswordWtform(BaseForm):
    account = StringField(validators=[DataRequired(message='账号不能为空')])
    password = StringField(validators=[DataRequired(message='密码不能为空')])
    password1 = StringField(validators=[DataRequired(message='新密码不能为空'), length(min=8, max=16, message='密码长度要求为8~16，请检查长度是否正确')])
    password2 = StringField(validators=[EqualTo('password1', message='两次密码不相同请重新输入')])


class AccessAccount(BaseForm):
    account = StringField(validators=[DataRequired(length(12, message='账号长度不正确请重新输入'))])
