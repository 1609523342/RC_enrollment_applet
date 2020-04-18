# 简易报名小程序

## 项目简介
该项目是使用python语言的flask框架实现的一个简单的报名程序的后端。
主要功能包括：报名表的增删改查，权限管理。后续会继续更新一些比较实用的功能
使该项目使用起来更加便捷更加贴合实际。

## 所需基础
需要熟悉python语言并且对flask框架有一定的了解。
数据库使用的是mysql数据库

## 使用说明
### 环境配置
MySQL (version: 5.6+)
Python (version: 3.5+)
编译器建议使用pycharm，社区版专业版均可

### 安装依赖包
建议安装pipenv创建虚拟环境
安装命令：
```shell
pipenv shell
```
pip install pipenv
然后在项目根目录输入：
```shell
pipenv shell
```
之后会显示该虚拟环境的名字，再去到pycharm的setting去以下路径找到环境
```shell
C:\Users\Administrator\.virtualenvs\虚拟环境名字\Scripts\python.exe
```
在Terminal下先输入
```shell
pipenv shell
```
然后再输入
```shell
pip install -r requirements
```
环境配置完成
### 修改配置文件
配置文件在app目录下的config.py文件中
SQLALCHEMY_DATABASE_URI为连接数据库的配置
配置示例：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@数据库地址:端口号'
```
设置token过期时间，WX_TIME为小程序的token，WEB_TIME为网页版的token
```python
WX_TIME = 60*60*24*30
WEB_TIME = 60*60*24
```
ROOT_AND_DEPARTMENT_NAME具体权限名，第一个默认为最高权限的权限名，ROOT为权限等级的权限名
```python
ROOT_AND_DEPARTMENT_NAME = ['实验室负责人', 'Android', 'Python', 'UI设计组', '微信小程序', 'web前端', 'Java', '普通用户']
ROOT = ['普通用户', '部长', '管理员']
```
SECRET_KEY为生成token的秘钥，可以自定义，但建议长度应该在20个字符以上

APPID、SECRET、JS_CODE、GRANT_TYPE为微信登录获取openid的必备参数，请参阅微信的开放文档
文档地址：

https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html

### 运行
在Terminal下先输入
```shell
pipenv shell
```
然后再输入
```shell
python run.py
```
若显示：
```shell
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
则运行成功
### 请求携带token
token的构造有两种方式，第一种是通过访问微信的登录接口获取openid来构造token,该token必须以

token:XXX

放在headers里。

若是采用网页登录的形式，则token会直接写入cookies，并且在浏览器不关闭之前都有效（若是设置了token有效时间则会按照有效时间，到期失效）