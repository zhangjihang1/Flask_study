from datetime import datetime

from apps import db


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    psw = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(120), unique=True, nullable=False)
    birthday = db.Column(db.DATE, nullable=False)
    introduction = db.Column(db.TEXT)
    uuid = db.Column(db.String(120), unique=True, nullable=False)
    face = db.Column(db.String(255), unique=True, nullable=False)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.name

    def check_psw(self, psw):
        return self.psw == psw


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
