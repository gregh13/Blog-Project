import requests
import smtplib

MY_EMAIL = "pythonnoob222@gmail.com"
MY_PASSWORD = "Udemy2022!"

STOCK_PRICE_API_KEY = "O56AP5TQVQ5BAZUG"
parameters_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "FB",
    "apikey": STOCK_PRICE_API_KEY
}

STOCK_NEWS_API_KEY = "OUbYDfahrs8Rc5gUtEBWtia3pX1MsrlOTH8rvijd"
parameters_news = {
    "symbols": "FB",
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
                            msg=f"Subject:Hello! It's Flight Deal Time :)\n\nSnippet1: {first_snippet}"
                            )