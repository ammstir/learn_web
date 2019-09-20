from flask import Flask, render_template, flash, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)

from .weather import weather_by_city
from .model import db, News, Users
from .forms import LoginForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    @app.route("/")
    def index():
        page_title = "Новости Python"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = News.query.order_by(News.published.desc()).all()

        return render_template(
            "index.html", page_title=page_title, weather=weather, news_list=news_list
        )

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        title = "Авторизация"
        login_form = LoginForm()

        return render_template("login.html", page_title=title, form=login_form)

    @app.route("/process-login", methods=["POST"])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = Users.query.filter(Users.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Вы успешно вошли на сайт")
                return redirect(url_for("index"))

        flash("Неправильные имя или пароль")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        logout_user()
        flash("Вы успешно разлогинились")
        return redirect(url_for("index"))

    @app.route("/admin")
    @login_required
    def admin_index():
        if current_user.is_admin:
            return "Привет, админ"
        else:
            return "Ты не админ"

    return app
