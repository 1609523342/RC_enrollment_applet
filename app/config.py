DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0203121516@localhost:3306/app'
APPID = 'wx4383a2432bd7ab15'
SECRET = 'f83937de86bd2774a6f819b970e0bd43'
GRANT_TYPE = 'authorization_code'
SECRET_KEY = 'WERQTHJOPNVALSHIOGRLNVUAGASLRJGKLANSVIONLASRKNN'
WX_TIME = 60*60*24*30
WEB_TIME = 60*60*24
ROOT_AND_DEPARTMENT_NAME = ['实验室负责人', 'Android', 'Python', 'UI设计组', '微信小程序', 'web前端', 'Java', '普通用户']
ROOT = ['普通用户', '部长', '管理员']
INVITATION_CODE = '123456789'
WX_LOGIN_API = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&grant_type={GRANT_TYPE}'.format(APPID=APPID, SECRET=SECRET, GRANT_TYPE=GRANT_TYPE)
