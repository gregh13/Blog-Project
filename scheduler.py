import requests
from twilio.rest import Client




TWILIO_SID = "AC8bc707c746ed8ab418ed99dd5d237569"
TWILIO_TOKEN = "02611c2364d604e7e9e16816f7b675ef"
TWILIO_PHONE = "+17402400638"
PHONE_NUM = "+66991132024"
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

    account_sid = TWILIO_SID
    auth_token = TWILIO_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"---------\n\n{parameters_news['symbols']}: {sms_num}   "
             f"\nLatest Close Price: ${two_day_close_list[0]}   "
             f"\nDay Early Close: ${two_day_close_list[1]}   "
             f"\n--------\n"
             f"Snippet1: {first_snippet}"
             f"\n--------\n"
             f"Snippet2: {second_snippet}",
        from_=TWILIO_PHONE,
        to=PHONE_NUM,
    )