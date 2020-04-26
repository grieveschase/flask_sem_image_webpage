from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class PasswordForm(FlaskForm):
    new_password = StringField('New Pass', validators=[DataRequired(), Length(1, 64)])
    role_id_field = SelectField("Role ID: ", choices=[(1, "Normal User"), (2, "Administrator")],  coerce=int)
    submit = SubmitField('Change Password')

class NewUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    password = StringField('Password', validators=[DataRequired(), Length(1, 64)])
    role_id_field = SelectField("Role ID: ", choices=[(1, "Normal User"), (2, "Administrator")],  coerce=int)
    submit = SubmitField('Create User')


class RemoveUserForm(FlaskForm):
    submit = SubmitField('Delete User')
