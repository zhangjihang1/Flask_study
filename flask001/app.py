import sqlite3
from functools import wraps

from flask import Flask, render_template, url_for, request, redirect, g, flash, session, make_response

from model import User

app = Flask(__name__)
app.debug = True
app.config["DATABASE"] = 'database.db'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


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


def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('user_login', next=request.url))  # 满足条件后的跳转页面
        return f(*args, **kwargs)

    return decorated_function


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
@user_login_req
def index():
    users = query_users_from_db()
    for user in users:
        print(user.toList())
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['user_name']
        userpsw = request.form['user_psw']
        # 查看用户是否存在
        user_x = query_user_by_name(username)
        if not user_x:
            flash(message='用户名不存在！', category='error')
            return redirect(url_for('user_register'))
        else:
            if userpsw != user_x.psw:
                flash(message='用户密码错误!', category='error')
                return redirect(url_for('user_login', username=user_x.name))
            else:
                # flash(message='登录成功!', category='ok')
                session['user_name'] = user_x.name
                return redirect(url_for('index'))
    return render_template('user_login.html')


@app.route('/logout/', methods=['GET', 'POST'])
@user_login_req
def user_logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        user = User()
        user.name = request.form['user_name']
        user.psw = request.form['user_psw']
        user.email = request.form['user_email']
        user.age = request.form['user_age']
        user.birthday = request.form['user_birthday']
        user.face = request.form['user_face']
        # 查看用户是否存在
        user_x = query_user_by_name(user.name)
        if user_x:
            flash(message='用户名已经存在！', category='error')
            return redirect(url_for('user_register'))
        # 如果用户不存在执行插入操作
        insert_user_to_db(user)
        flash(message='注册成功！', category='ok')
        return redirect(url_for('user_login', username=user.name))
    return render_template('user_register.html')


@app.route('/center/', methods=['GET', 'POST'])
@user_login_req
def user_center():
    return render_template('user_center.html')


@app.route('/detail/')
@user_login_req
def user_detail():
    user = query_user_by_name(session.get('user_name'))
    return render_template('user_detail.html', user=user)


@app.route('/psw/', methods=['GET', 'POST'])
@user_login_req
def user_psw():
    if request.method == 'POST':
        old_psw = request.form['old_psw']
        new_psw = request.form['new_psw']
        user = query_user_by_name(session.get('user_name'))
        if old_psw == user.psw:
            user.psw = new_psw
            update_user_by_name(user.name, user)
            session.pop('user_name', None)
            flash(message='密码修改成功，请重新登录！', category='ok')
            return redirect(url_for('user_login', username=user.name))
        else:
            flash(message='输入的旧密码不对！', category='error')
            return render_template('user_psw.html')
    return render_template('user_psw.html')


@app.route('/info/', methods=['GET', 'POST'])
@user_login_req
def user_info():
    user = query_user_by_name(session.get('user_name'))
    if request.method == 'POST':
        old_name = user.name
        user.name = request.form['user_name']
        user.email = request.form['user_email']
        user.age = request.form['user_age']
        user.birthday = request.form['user_birthday']
        user.face = request.form['user_face']
        update_user_by_name(old_name, user)
        session['user_name'] = user.name
        return redirect(url_for('user_detail', user=user))
    return render_template('user_info.html', user=user)


@app.route('/del/', methods=['GET', 'POST'])
@user_login_req
def user_del():
    if request.method == 'POST':
        del_user_by_name(session.get('user_name'))
        return redirect(url_for('user_logout'
                                ''))
    return render_template('user_del.html')


@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


if __name__ == '__main__':
    app.run()
