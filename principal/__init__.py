from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from principal.admin_views import MyAdminIndexView

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "7829d62f6ae53e182b766db738d2b556"


# Mock babel to prevent KeyError
class MockBabel:
    def __init__(self, app):
        self.locale_selector = None
        self.instance = self
        self.default_locale = "en"
        self.default_timezone = "UTC"

    def localeselector(self, f):
        self.locale_selector = f
        return f


app.extensions = app.extensions or {}
app.extensions["babel"] = MockBabel(app)

database = SQLAlchemy(app)
admin = Admin(index_view=MyAdminIndexView())
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
admin.init_app(app)

from principal.admin_views import AdminView
from principal.models import User, Post

admin.add_view(AdminView(User, database.session))
admin.add_view(AdminView(Post, database.session))

from principal import views
