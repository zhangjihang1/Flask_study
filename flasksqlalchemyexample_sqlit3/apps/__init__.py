from flask import Flask

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

import apps.views
