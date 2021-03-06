from flask_uploads import IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空'),
                    Length(min=3, max=15, message='用户名在3到15个字符之间！')],
        render_kw={'id': "user_name",
                   'class': "form-control",
                   'placeholder': '请输入用户名'}
    )
    user_psw = PasswordField(
        label='用户密码',
        validators=[DataRequired(message='用户密码不能为空'),
                    Length(min=3, max=6, message='用户密码在3到6个字符之间！')],
        render_kw={'id': "user_psw",
                   'class': "form-control",
                   'placeholder': '请输入用户密码'}
    )
    user_email = StringField(
        label='用户邮箱',
        validators=[DataRequired(message='用户邮箱不能为空'),
                    Email(message='用户邮箱格式不正确')],
        render_kw={'id': "user_email",
                   'class': "form-control",
                   'placeholder': '请输入用户邮箱'}
    )
    user_telephone = StringField(
        label='用户电话',
        validators=[DataRequired(message='用户手机不能为空')],
        render_kw={'id': "user_telephone",
                   'class': "form-control",
                   'placeholder': '请输入用户手机'}
    )
    user_birthday = StringField(
        label='用户生日',
        validators=[DataRequired(message='用户生日不能为空')],
        render_kw={'id': "user_birthday",
                   'class': "form-control",
                   'placeholder': '请输入用户生日'}
    )
    user_introduction = TextAreaField(
        label='用户简介',
        validators=[],
        render_kw={'id': "user_introduction",
                   'class': "form-control",
                   'placeholder': '请输入用户简介'}
    )
    user_face = FileField(
        label='用户头像',
        validators=[FileRequired(message='用户头像不能为空'),
                    FileAllowed(IMAGES, '只允许图像格式为：%s' % str(IMAGES))],
        render_kw={'id': "user_face",
                   'class': "form-control",
                   'placeholder': '请输入用户头像'}
    )
    submit = SubmitField(
        label='提交表单',
        render_kw={'class': "bnt bnt-success",
                   'value': '注册'}
    )


class LoginForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空')],
        render_kw={'id': "user_name",
                   'class': "form-control",
                   'placeholder': '请输入用户名'}
    )
    user_psw = PasswordField(
        label='用户密码',
        validators=[DataRequired(message='用户密码不能为空')],
        render_kw={'id': "user_psw",
                   'class': "form-control",
                   'placeholder': '请输入用户密码'}
    )
    submit = SubmitField(
        label='提交表单',
        render_kw={'class': "bnt bnt-success",
                   'value': '登录'}
    )


class PswForm(FlaskForm):
    old_psw = StringField(
        label='旧密码',
        validators=[DataRequired(message='旧密码不能为空')],
        render_kw={'id': "old_psw",
                   'class': "form-control",
                   'placeholder': '请输入用户旧密码'}
    )
    new_psw = StringField(
        label='新密码',
        validators=[DataRequired(message='新密码不能为空')],
        render_kw={'id': "new_psw",
                   'class': "form-control",
                   'placeholder': '请输入用户新密码'}
    )
    submit = SubmitField(
        label='提交表单',
        render_kw={'class': "bnt bnt-success",
                   'value': '修改'}
    )


class InfoForm(FlaskForm):
    user_name = StringField(
        label='用户名',
        validators=[DataRequired(message='用户名不能为空'),
                    Length(min=3, max=15, message='用户名在3到15个字符之间！')],
        render_kw={'id': "user_name",
                   'class': "form-control",
                   'placeholder': '请输入用户名'}
    )
    user_email = StringField(
        label='用户邮箱',
        validators=[DataRequired(message='用户邮箱不能为空'),
                    Email(message='用户邮箱格式不正确')],
        render_kw={'id': "user_email",
                   'class': "form-control",
                   'placeholder': '请输入用户邮箱'}
    )
    user_telephone = IntegerField(
        label='用户电话',
        validators=[DataRequired(message='用户电话不能为空')],
        render_kw={'id': "user_telephone",
                   'class': "form-control",
                   'placeholder': '请输入用户电话'}
    )
    user_birthday = StringField(
        label='用户生日',
        validators=[DataRequired(message='用户生日不能为空')],
        render_kw={'id': "user_birthday",
                   'class': "form-control",
                   'placeholder': '请输入用户生日'}
    )
    user_introduction = TextAreaField(
        label='用户简介',
        validators=[],
        render_kw={'id': "user_introduction",
                   'class': "form-control",
                   'placeholder': '请输入用户简介'}
    )
    user_face = FileField(
        label='用户头像',
        validators=[FileAllowed(IMAGES, '只允许图像格式为：%s' % str(IMAGES))],
        render_kw={'id': "user_face",
                   'class': "form-control",
                   'placeholder': '请输入用户头像'}
    )
    submit = SubmitField(
        label='提交表单',
        render_kw={'class': "bnt bnt-success",
                   'value': '修改'}
    )


class DelForm(FlaskForm):
    submit = SubmitField(
        label='提交表单',
        render_kw={'class': "bnt bnt-success",
                   'value': '注销'}
    )
