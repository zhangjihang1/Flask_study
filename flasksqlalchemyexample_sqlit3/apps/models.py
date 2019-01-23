from flask_sqlalchemy import SQLAlchemy

from apps import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r, Email %r>' % (self.username, self.email)


if __name__ == '__main__':
    db.create_all()
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    all = User.query.all()
    print(all)
    admin_xx = User.query.filter_by(username='admin').first()
    print(admin_xx)
