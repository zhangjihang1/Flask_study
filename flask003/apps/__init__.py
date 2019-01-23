import os


from flask import Flask

from apps.tools import create_folder

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


APPS_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(APPS_DIR, 'static')

app.config["DATABASE"] = os.path.join(APPS_DIR, 'database.db')
app.config["UPLOADS_RELATIVE"] = 'uploads'
app.config["UPLOADS_FOLDER"] = os.path.join(STATIC_DIR, app.config["UPLOADS_RELATIVE"])
# app.config["UPLOADS_FOLDER"] = os.path.join(STATIC_DIR, 'uploads')

create_folder(app.config["UPLOADS_FOLDER"])

import apps.views
