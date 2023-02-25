import requests
import pandas as pd
import os
import dotenv
import datetime as dt
from twilio.rest import Client

dotenv.load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
URL = "https://www.alphavantage.co/query"
params_stock = {
    "function":"TIME_SERIES_INTRADAY",
    "symbol":STOCK,
    "interval":"60min",
    "apikey":os.environ["ALPHAVANTAGE_API_KEY"]
}

response = requests.get(url=URL, params=params_stock)
response.raise_for_status()
data = response.json()
last_refresh = data['Meta Data']["3. Last Refreshed"]
date_time_obj = dt.datetime.strptime(last_refresh, '%Y-%m-%d %H:%M:%S')
day_before = date_time_obj - dt.timedelta(days=1)

data_yesterday = float(data["Time Series (60min)"][last_refresh]["4. close"])
data_day_before = float(data["Time Series (60min)"][str(day_before)]["4. close"])

change = (data_yesterday - data_day_before)/data_yesterday * 100


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if abs(change) >= 0:
    url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={last_refresh}&sortBy=popularity&apiKey={os.environ['NEWS_API']}"
    news_response = requests.get(url)
    news_response.raise_for_status()
    data = news_response.json()
    articles = list(data['articles'][:3])

    #Sending the message
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    for i in articles:
        message = client.messages \
            .create(
            body=f"{STOCK}: {round(change, 2)}%\n"
                 f"Headline: {i['title']}\n"
                 f"Link: {i['url']}",
            from_=os.environ["TWILIO_NO"],
            to=os.environ["MY_NO"]
        )
        print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

