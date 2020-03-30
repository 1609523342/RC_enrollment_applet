from app.forms.error import APIException


class Success(APIException):
    code = 200
    msg = "上传成功"
    error_code = 1000


class ParameterException(APIException):
    code = 400
    msg = "参数错误"
    error_code = 1001


class AuthException(APIException):
    code = 401
    msg = '令牌验证失效'
    error_code = 1002


class TokenException(APIException):
    code = 401
    msg = '令牌缺失'
    error_code = 1003


class SQLException(APIException):
    code = 500
    msg = '数据写入数据库出错'
    error_code = 1004


class SQLMissException(APIException):
    code = 500
    msg = '数据库查询数据出错'
    error_code = 1005


class RootException(APIException):
    code = 401
    msg = '您无此操作权限'
    error_code = 1006


class LoginException(APIException):
    code = 401
    msg = '网页登录出错'
    error_code = 1007