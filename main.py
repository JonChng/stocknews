import requests
import pandas as pd
import os
import dotenv
import datetime as dt

yesterday = str(dt.date.today() - dt.timedelta(days=1))
yesterday_closing = yesterday + " 20:00:00"

day_before = str(dt.date.today() - dt.timedelta(days=2))
day_before_closing = day_before + " 20:00:00"


dotenv.load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
URL = "https://www.alphavantage.co/query"
params = {
    "function":"TIME_SERIES_INTRADAY",
    "symbol":STOCK,
    "interval":"60min",
    "apikey":os.environ["ALPHAVANTAGE_API_KEY"]
}

response = requests.get(url=URL, params=params)
response.raise_for_status()
data = response.json()
data_yesterday = float(data["Time Series (60min)"][yesterday_closing]["4. close"])
data_day_before = float(data["Time Series (60min)"][day_before_closing]["4. close"])

change = (data_yesterday - data_day_before)/data_yesterday * 100


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


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

