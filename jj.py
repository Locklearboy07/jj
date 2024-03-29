@app.route('/')
def hello():
    return 'Hello, World!'

import bitmart
import talib
from flask import Flask, jsonify
from bitmart.api_spot import APISpot

api_key = "039c26c7f5316ab9891ed924b3a4885bf35c70fe"
secret_key = "866cee39cb5a66816c815ee46481530f4d6b984bcf8eb9f9676715ee46fe2e37"
memo = "5"
url = "https://api-cloud.bitmart.com/spot/v1/ticker_detail"
api = APISpot(api_key, secret_key, memo, url)

app = Flask(__name__)

@app.route('/current_price')
def get_current_price():
    ticker = api.get_ticker('xlm_usdT')
    return jsonify(ticker['last_price'])

@app.route('/moving_average')
def calculate_moving_average():
    prices = api.get_candlestick('xlm_usdT', '1h', 21)
    close_prices = [float(price['close']) for price in prices['data']]
    moving_average = talib.SMA(close_prices, timeperiod=20)
    return jsonify(moving_average[-1])

@app.route('/bollinger_bands')
def calculate_bollinger_bands():
    prices = api.get_candlestick('xlm_usdT', '1h', 21)
    close_prices = [float(price['close']) for price in prices['data']]
    upper_band, middle_band, lower_band = talib.BBANDS(close_prices, timeperiod=20)
    return jsonify(upper_band[-1], middle_band[-1], lower_band[-1])

@app.route('/buy_xlm/<price>')
def buy_xlm(price):
    api.create_order('xlm_usdtT', 'limit', 'buy', price, '100')
    return jsonify(message="Buy order placed")

@app.route('/sell_xlm/<price>')
def sell_xlm(price):
    api.create_order('xlm_usdtT', 'limit', 'sell', price, '100')
    return jsonify(message="Sell order placed")

if __name__ == '__main__':
    app.run()
