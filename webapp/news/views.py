from flask import render_template, Blueprint, current_app
from webapp.weather import weather_by_city
from webapp.news.models import News

bp = Blueprint("news", __name__)


@bp.route("/")
def index():
    page_title = "Новости Python"
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    news_list = News.query.order_by(News.published.desc()).all()

    return render_template(
        "news/index.html", page_title=page_title, weather=weather, news_list=news_list
    )