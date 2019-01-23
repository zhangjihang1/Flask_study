import os
import shutil
from functools import wraps

from flask import session, redirect, request, url_for, render_template, flash, make_response, g
from flask_uploads import UploadSet, IMAGES, configure_uploads, UploadNotAllowed

from apps import app
from apps.db_manage import connect_db, query_user_by_name, query_users_from_db, insert_user_to_db, update_user_by_name, \
    del_user_by_name
from apps.form import LoginForm, RegisterForm, PswForm, InfoForm, DelForm
from apps.model import User
from apps.tools import secure_filename_with_uuid, check_files_extensions, ALLOWED_IMAGE_EXTENSIONS

photos = UploadSet(name='photos', extensions=IMAGES)

configure_uploads(app, (photos,))


def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('user_login', next=request.url))  # 满足条件后的跳转页面
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    users = query_users_from_db()
    for user in users:
        print(user.toList())
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
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
                return redirect(url_for('user_login', form=form, username=user_x.name))
            else:
                # flash(message='登录成功!', category='ok')
                session['user_name'] = user_x.name
                return redirect(url_for('index'))
    return render_template('user_login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@user_login_req
def user_logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 检查用户上传的头像文件是否符合要求
        # if not check_files_extensions([form.user_face.data.filename], ALLOWED_IMAGE_EXTENSIONS):
        #     flash(message='头像格式不正确！', category='error')
        #     return redirect(url_for('user_register', form=form))
        user_name = request.form.get('user_name')
        # 查看用户是否存在
        user_x = query_user_by_name(user_name)
        # 如果用户存在
        if user_x:
            flash(message='用户名已经存在！', category='error')
            return redirect(url_for('user_register', form=form))
        # 如果用户不存在，执行注册
        user = User()
        user.name = request.form.get('user_name')
        user.psw = request.form.get('user_psw')
        user.email = request.form.get('user_email')
        user.age = request.form.get('user_age')
        user.birthday = request.form.get('user_birthday')
        f_face = request.files['user_face']
        user.face = secure_filename_with_uuid(f_face.filename)
        insert_user_to_db(user)
        # 保存用户名
        # user_folder = os.path.join(app.config["UPLOADS_FOLDER"], user.name)
        # create_folder(user_folder)
        # f_face.save(os.path.join(user_folder, user.face))
        try:
            photos.save(storage=f_face, folder=user.name, name=user.face)
            flash(message='注册成功！', category='ok')
            return redirect(url_for('user_login', username=user.name))
        except UploadNotAllowed:
            flash(message='用户头像格式不对！', category='error')
            return render_template('user_register.html', form=form)

    return render_template('user_register.html', form=form)


@app.route('/center/', methods=['GET', 'POST'])
@user_login_req
def user_center():
    return render_template('user_center.html')


@app.route('/detail/')
@user_login_req
def user_detail():
    user = query_user_by_name(session.get('user_name'))
    # uploads_folder = app.config["UPLOADS_RELATIVE"]
    face_url = photos.url(user.name + '/' + user.face)
    return render_template('user_detail.html', user=user, face_url=face_url)


@app.route('/psw/', methods=['GET', 'POST'])
@user_login_req
def user_psw():
    form = PswForm()
    if form.validate_on_submit():
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
            return render_template('user_psw.html', form=form)
    return render_template('user_psw.html', form=form)


@app.route('/info/', methods=['GET', 'POST'])
@user_login_req
def user_info():
    form = InfoForm()
    user = query_user_by_name(session.get('user_name'))
    if form.validate_on_submit():
        old_name = user.name
        user.name = request.form['user_name']
        user.email = request.form['user_email']
        user.age = request.form['user_age']
        user.birthday = request.form['user_birthday']
        f_face = form.user_face.data
        if f_face != '':
            # 检查用户上传的头像文件是否符合要求
            # if not check_files_extensions([form.user_face.data.filename], ALLOWED_IMAGE_EXTENSIONS):
            #     flash(message='头像格式不正确！', category='error')
            #     return redirect(url_for('user_info'))
            # user_folder = os.path.join(app.config['UPLOADS_FOLDER'], old_name)
            face_path = photos.path(filename=user.face, folder=old_name)
            os.remove(path=face_path)
            user.face = secure_filename_with_uuid(f_face.filename)
            photos.save(storage=f_face, folder=old_name, name=user.face)
        if old_name != user.name:
            os.rename(os.path.join(app.config['UPLOADS_FOLDER'], old_name),
                      os.path.join(app.config['UPLOADS_FOLDER'], user.name))
        update_user_by_name(old_name, user)
        session['user_name'] = user.name
        return redirect(url_for('user_detail', user=user))
    return render_template('user_info.html', user=user, form=form)


@app.route('/del/', methods=['GET', 'POST'])
@user_login_req
def user_del():
    form = DelForm()
    if form.validate_on_submit():
        # 删除用户上传的资源
        del_path = os.path.join(app.config["UPLOADS_FOLDER"], session.get('user_name'))
        shutil.rmtree(del_path, ignore_errors=True)
        del_user_by_name(session.get('user_name'))
        return redirect(url_for('user_logout'))
    return render_template('user_del.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
