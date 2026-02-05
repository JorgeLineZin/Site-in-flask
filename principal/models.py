from principal import database, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from principal import admin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True, unique=True)
    name = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    is_admin = database.Column(database.Boolean, nullable=False, default=False)
    posts = database.relationship("Post", backref="user", lazy=True)

    def __str__(self):
        return self.name


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True, unique=True)
    title = database.Column(database.String, nullable=False)
    content = database.Column(database.Text, nullable=False)
    created_date = database.Column(
        database.DateTime(timezone=True), default=datetime.utcnow
    )
    id_user = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=False
    )



