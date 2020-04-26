from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
#from ..email import send_email
from .forms import LoginForm, PasswordForm, NewUserForm, RemoveUserForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            session.permanent = True
            return redirect(url_for('main.index'))
        flash('Invalid name or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/user-names', methods=['GET'])
@login_required
def user_names():
    if not current_user.is_administrator():
        return redirect(url_for('main.index'))
    users = User.query.with_entities(User.name, User.role_id).all()

    return render_template('auth/user_names.html', users = users)

@auth.route('/user-edit/<user>', methods=['GET','POST'])
@login_required
def user_edit(user):
    if not current_user.is_administrator():
        return redirect(url_for('main.index'))
    form = PasswordForm()
    form_delete = RemoveUserForm()
    if form.validate_on_submit():
        user_object = User.query.filter_by(name = user).first()
        if user_object is not None:
            user_object.password = form.new_password.data
            user_object.role_id = form.role_id_field.data
            db.session.add(user_object)
            db.session.commit()
            flash('Password for "%s" has been changed'%user_object.name)
            return redirect(url_for('.user_names'))
    if form_delete.validate_on_submit():
        user_object = User.query.filter_by(name = user).first()
        db.session.delete(user_object)
        db.session.commit()
        flash('User "%s" has been deleted'%user_object.name)
        return redirect(url_for('.user_names'))
    return render_template('auth/user_edit.html', user=user, form = form, form_delete=form_delete)


@auth.route('/user-add', methods=['GET','POST'])
@login_required
def user_add():
    if not current_user.is_administrator():
        return redirect(url_for('main.index'))
    form = NewUserForm()
    if form.validate_on_submit():
        user_object = User.query.filter_by(name = form.name.data).first()
        if user_object is None:
            new_user = User(name=form.name.data, password=form.password.data, role_id = form.role_id_field.data)
            db.session.add(new_user)
            db.session.commit()
            flash('New user "%s" has been added'%form.name.data)
            return redirect(url_for('.user_add'))
        else:
            flash('Username "%s" is already in use!'%form.name.data)
            return redirect(url_for('.user_add'))

    return render_template('auth/user_add.html', form = form)











#
