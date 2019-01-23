from flask_sqlalchemy import SQLAlchemy

from apps import app

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.personname


class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class AppMeta(db.Model):
    __bind_key__ = 'appmeta'
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(80), unique=True, nullable=False)
    info = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<AppMeta %r>' % self.appname


if __name__ == '__main__':
    db.create_all()
    # admin = User(username='admin', email='admin@example.com')
    # guest = User(username='guest', email='guest@example.com')
    # peter = User(username='peter', email='peter@example.org')
    # db.session.add(admin)
    # db.session.add(guest)
    # db.session.add(peter)
    # db.session.commit()
    # all = User.query.all()
    # print(all)
    # admin_xx1 = User.query.filter_by(username='admin').first()
    # print(admin_xx1)
    # admin_xx2 = User.query.filter(User.email.endswith('@example.com')).all()
    # print(admin_xx2)
