from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, current_user

from webapp.user.models import User
from webapp.user.forms import LoginForm

bp = Blueprint("user", __name__, url_prefix="/users")


@bp.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("news.index"))
    title = "Авторизация"
    login_form = LoginForm()

    return render_template("user/login.html", page_title=title, form=login_form)


@bp.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно вошли на сайт")
            return redirect(url_for("news.index"))

    flash("Неправильные имя или пароль")
    return redirect(url_for("user.login"))


@bp.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("news.index"))
