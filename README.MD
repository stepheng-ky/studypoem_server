# 微信小程序-一木古诗词后端
**主要功能是提供学习古诗词相关服务**  
对应的微信小程序：https://github.com/stepheng-ky/studyPoem  

## 0、TODO
1. 微信授权功能
2. 所有接口添加权限认证
3. poem_details接口添加返回背景图
4. 新增、复制、删除、重命名计划功能
5. 计划新增、删除诗词功能
6. 计划中诗词排序功能
7. 个人信息显示、修改
8. 收藏诗词、查询已收藏诗词
9. 已学习诗词列表查询
10. 诗词详情，新增朗诵语音
11. 打卡新增上传语音音频
12. 播放诗词语音、个人上传的语音功能
13. 

## 1、目录结构
.  
├── app  
│   ├── app.py  
│   ├── config.py  
│   ├── __init__.py  
│   ├── models  
│   │   ├── category.py  
│   │   ├── __init__.py  
│   │   ├── plan.py  
│   │   ├── poem.py  
│   │   └── user.py  
│   ├── nohup.out  
│   ├── routes.py  
│   ├── services  
│   │   ├── category_service.py  
│   │   ├── __init__.py  
│   │   ├── plan_service.py  
│   │   ├── poem_service.py  
│   │   └── user_service.py  
│   └── utils.py  
├── __init__.py  
└── README.MD  
  

## 2、环境准备
### python环境
**版本**：python3.10  
**依赖**：  
pip3 install flask  
pip3 install Flask-SQLAlchemy  
pip3 install PyMySQL  
pip3 install requests  

### mysql安装
### prod-部署uwsgi、配置https、nginx等

## 3、部署服务

1. 在项目目录下维护config.py中的数据库信息   :
```
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Config:
    # 数据库信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@ip/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 微信小程序信息
    APPID = 'APPID'
    APPSECRET = 'APPSECRET'

    # 微信接口域名
    WX_API_URL = 'https://api.weixin.qq.com'
```
其中微信小程序的APPID、APPSECRET需要自行申请：
https://mp.weixin.qq.com/  ,登录之后，左侧 开发-->开发管理-->开发设置-->开发者ID-->可以看到AppID、生成AppSecret。  

2. app目录下创建logs目录  
3. git clone
4. 启动服务：  
本地：python -m app.app  
prod：启动uwsgi、nginx   
5. 访问服务：http://127.0.0.1:5000
