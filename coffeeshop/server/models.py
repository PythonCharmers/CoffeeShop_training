"""
User and role models

As per Flask-Security with the addition of a screen name on the user model.
"""
from flask_security import UserMixin, RoleMixin

from coffeeshop.server import db


class RolesUsers(db.Model):
    """Many to many relationship table"""
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    """
    Application roles

    It's worth noting that these aren't the same as the roles in the database.
    The application will only connect with the role provided in the connection
    string and will execute with those privileges.
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Role {0}>".format(self.name)


class User(db.Model, UserMixin):
    """
    User model

    The vast majority of this information is metadata that is never seen by the
    user, but is useful for monitoring and debugging.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    screen_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        'Role',
        secondary='roles_users',
        backref=db.backref('users', lazy='dynamic')
    )

    def __repr__(self):
        return "<User {0}>".format(self.email)
