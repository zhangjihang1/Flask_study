from flask import Flask

app = Flask(__name__)
app.debug = True

# dialect+driver://username:password@host:port/database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasker.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flasker'
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'mysql+pymysql://root:123456@localhost/users',
    'appmeta': 'sqlite:///appmeta.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

import apps.views
