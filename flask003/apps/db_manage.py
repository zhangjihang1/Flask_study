import sqlite3

from flask import g

from apps import app
from apps.model import User


def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db


def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def insert_user_to_db(user):
    # sql_insert = 'insert into users (name, psw, email, age, birthday, face) values (?, ?, ?, ?, ?, ?)'
    user_attrs = user.getAttrs()
    values = 'values ('
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            values += ' ?,'
        else:
            values += ' ?'
    values += ' )'
    sql_insert = 'insert into users ' + str(user_attrs) + values
    # args = [user.name, user.psw, user.email, user.age, user.birthday, user.face]
    args = user.toList()
    g.db.execute(sql_insert, args)
    g.db.commit()


def query_users_from_db():
    users = []
    sql_select = 'select * from users'
    args = []
    cur = g.db.execute(sql_select, args)
    for item in cur.fetchall():
        user = User()
        user.fromList(item[1:])
        users.append(user)
    return users


def query_user_by_name(user_name):
    sql_select = 'select * from users where name=?'
    args = [user_name]
    cur = g.db.execute(sql_select, args)
    items = cur.fetchall()
    if len(items) < 1:
        return None
    first_item = items[0]
    user = User()
    user.fromList(first_item[1:])
    return user


def del_user_by_name(user_name):
    sql_del = 'delete from users where name=?'
    args = [user_name]
    g.db.execute(sql_del, args)
    g.db.commit()


def update_user_by_name(old_name, user):
    # UPDATE Person SET FirstName = 'Fred', city = 'beijing' WHERE LastName = 'Wilson'
    update_str = ''
    user_attrs = user.getAttrs()
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            update_str += attr + ' = ?,'
        else:
            update_str += attr + ' = ?'
    sql_update = 'update users set ' + update_str + 'where name = ?'
    args = user.toList()
    args.append(old_name)
    g.db.execute(sql_update, args)
    g.db.commit()


if __name__ == '__main__':
    init_db()
