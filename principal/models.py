from principal import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True, unique=True)
    name = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship('Post', backref='user', lazy=True)

    
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True, unique=True)
    title = database.Column(database.String, nullable=False)
    content = database.Column(database.Text, nullable=False)
    created_date = database.Column(database.DateTime, default=datetime.utcnow())
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)