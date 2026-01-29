from principal import database, app
from principal.models import User, Post

with app.app_context():
    database.create_all()