from flask import Flask
from flask_login import LoginManager

from .weather import weather_by_city
from .db import db
from webapp.user.models import User
from webapp.user.forms import LoginForm
from webapp.user.views import bp as user_bp
from webapp.admin.views import bp as admin_bp
from webapp.news.views import bp as news_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(news_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

