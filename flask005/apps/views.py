import os
import shutil
import uuid
from functools import wraps

from flask import session, redirect, request, url_for, render_template, flash, make_response, g
from flask_uploads import UploadSet, IMAGES, configure_uploads, UploadNotAllowed

from apps import app
from apps import db
from apps.form import LoginForm, RegisterForm, PswForm, InfoForm, DelForm
from apps.models import User
from apps.tools import secure_filename_with_uuid

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
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['user_name']
        userpsw = request.form['user_psw']
        # 查看用户是否存在
        user_x = User.query.filter_by(name=username).first()
        if not user_x:
            flash(message='用户名不存在！', category='error')
            return redirect(url_for('user_register'))
        else:
            if user_x.check_psw(userpsw):
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
        user_x = User.query.filter_by(name=user_name).first()
        # 如果用户存在
        if user_x:
            flash(message='用户名已经存在！', category='error')
            return redirect(url_for('user_register', form=form))
        # 如果用户不存在，创建一个用户类的实例
        user = User()
        user.name = request.form.get('user_name')
        user.psw = form.user_psw.data
        user.email = request.form.get('user_email')
        user.telephone = request.form.get('user_telephone')
        user.birthday = request.form.get('user_birthday')
        user.introduction = request.form.get('user_introduction')
        user.uuid = str(uuid.uuid4().hex)[0:10]
        f_face = request.files['user_face']
        user.face = secure_filename_with_uuid(f_face.filename)
        # 保存用户名
        # user_folder = os.path.join(app.config["UPLOADS_FOLDER"], user.name)
        # create_folder(user_folder)
        # f_face.save(os.path.join(user_folder, user.face))
        try:
            photos.save(storage=f_face, folder=user.name, name=user.face)
            db.session.add(user)
            db.session.commit()
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
    user = User.query.filter_by(name=session.get('user_name')).first_or_404()
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
        user = User.query.filter_by(name=session.get('user_name')).first()
        if user.check_psw(old_psw):
            user.psw = new_psw
            db.session.add(user)
            db.session.commit()
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
    user = User.query.filter_by(name=session.get('user_name')).first()
    if form.validate_on_submit():
        old_name = user.name
        user.name = request.form['user_name']
        user.email = request.form['user_email']
        user.telephone = request.form['user_telephone']
        user.birthday = request.form['user_birthday']
        user.introduction = request.form.get('user_introduction')
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
        db.session.add(old_name, user)
        db.session.commit()
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
        user = User.query.filter_by(name=session.get('user_name')).first()
        db.session.delet(user)
        db.session.commit()
        return redirect(url_for('user_logout'))
    return render_template('user_del.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
