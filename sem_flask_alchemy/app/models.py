from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Permission:
    READ = 1
    ADMIN = 2

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ],
            'Administrator': [Permission.READ, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.name == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    @staticmethod
    def insert_users():
        names = ['ccag', 'other']
        pws = ['ccag123', 'other']
        for name, pw in zip(names, pws):
            user = User(name=name, password=pw)
            db.session.add(user)
            db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    def __repr__(self):
        return '<User %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class MeasDisplay_Obs(db.Model):
    __tablename__='measdisplay_obs'
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(64), index = True)
    slot = db.Column(db.Integer)
    fov = db.Column(db.Float)
    iprobe = db.Column(db.String(64))
    lot = db.Column(db.String(64), index=True)
    vacc =db.Column(db.Integer)
    vhar =db.Column(db.Integer)
    recipe = db.Column(db.String(64), index=True)
    site_type = db.Column(db.String(64))
    site_order = db.Column(db.Integer)
    fieldx = db.Column(db.Integer)
    fieldy = db.Column(db.Integer)
    locx = db.Column(db.Float)
    locy = db.Column(db.Float)
    date = db.Column(db.DateTime)
    port = db.Column(db.Integer)
    cycle = db.Column(db.Integer)
    target = db.Column(db.String(64))
    measdate = db.Column(db.DateTime)
    image = db.Column(db.LargeBinary)

class PatternFOV(db.Model):
    __tablename__='patternfov'
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(64), index = True)
    slot = db.Column(db.Integer)
    fov = db.Column(db.Float)
    iprobe = db.Column(db.String(64))
    lot = db.Column(db.String(64), index=True)
    vacc =db.Column(db.Integer)
    vhar =db.Column(db.Integer)
    recipe = db.Column(db.String(64), index=True)
    site_type = db.Column(db.String(64))
    site_order = db.Column(db.Integer)
    fieldx = db.Column(db.Integer)
    fieldy = db.Column(db.Integer)
    locx = db.Column(db.Float)
    locy = db.Column(db.Float)
    date = db.Column(db.DateTime)
    port = db.Column(db.Integer)
    cycle = db.Column(db.Integer)
    target = db.Column(db.String(64))
    measdate = db.Column(db.DateTime)
    image = db.Column(db.LargeBinary)

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
