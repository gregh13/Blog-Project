import requests
import smtplib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model, Base):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    # Can name these whatever, just need to be consistent
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")
    # Change schema to have ORM relationship
    # author = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


post = BlogPost.query.filter_by(id=2).first()
post_title = post.title

MY_EMAIL = "pythonnoob222@gmail.com"
MY_PASSWORD = "Udemy2022!"

STOCK_PRICE_API_KEY = "O56AP5TQVQ5BAZUG"
parameters_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": post_title,
    "apikey": STOCK_PRICE_API_KEY
}

STOCK_NEWS_API_KEY = "OUbYDfahrs8Rc5gUtEBWtia3pX1MsrlOTH8rvijd"
parameters_news = {
    "symbols": post_title,
    "language": "en",
    "filter_entities": "true",
    "api_token": STOCK_NEWS_API_KEY
}

# Gathers Stock Price Data
response_price = requests.get("https://www.alphavantage.co/query", params=parameters_price)
response_price.raise_for_status()
stock_price_data = response_price.json()["Time Series (Daily)"]

close_price_list = list(stock_price_data.items())
two_day_close_list = [float(x[1]["4. close"]) for x in close_price_list[:2]]
percent_change = round((two_day_close_list[0] - two_day_close_list[1]) / two_day_close_list[1], 3) * 100

if percent_change >= 0 or percent_change <= 0:
    if percent_change > 0:
        sms_num = str(percent_change) + "% ⬆️"
    if percent_change < 0:
        sms_num = str(percent_change) + "% ⬇️️"

    # Gathers Stock News to explain stock fluctuation
    response_news = requests.get(url="https://api.marketaux.com/v1/news/all", params=parameters_news)
    response_news.raise_for_status()
    stock_news = response_news.json()

    top_3_snippets = [x["snippet"] for x in stock_news["data"][:3]]
    first_snippet = top_3_snippets[0]
    second_snippet = top_3_snippets[1]

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=f"Subject:Hello! It's Stock Time: {post_title} :D\n\nPrice: {sms_num}\nSnippet1: {first_snippet}"
                            )