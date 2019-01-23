import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from apps.tools import create_folder

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

APPS_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(APPS_DIR, 'static')

# app.config["DATABASE"] = os.path.join(APPS_DIR, 'database.db')

# dialect+driver://username:password@host:port/database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasker.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flasker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

app.config["UPLOADS_RELATIVE"] = 'uploads'
app.config["UPLOADS_FOLDER"] = os.path.join(STATIC_DIR, app.config["UPLOADS_RELATIVE"])
# app.config["UPLOADS_FOLDER"] = os.path.join(STATIC_DIR, 'uploads')
# 第一步：配置上传文件保存地址
app.config["UPLOADED_PHOTOS_DEST"] = app.config["UPLOADS_FOLDER"]

create_folder(app.config["UPLOADS_FOLDER"])

import apps.views
