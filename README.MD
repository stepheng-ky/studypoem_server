# 主要功能是提供学习古诗词相关服务

## 环境准备
**python环境**：python3.10  
**依赖**：  
pip3 install flask  
pip3 install Flask-SQLAlchemy  
pip3 install PyMySQL  
pip3 install requests  

## 目录结构


## 部署服务
本地部署：  
python -m app.app  

远程部署：  
在项目目录下维护config.py中的数据库信息  
git pull最新代码  
python -m app.app 