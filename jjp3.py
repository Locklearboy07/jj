import os
from flask import Flask, jsonify
import bitmart
import talib
from bitmart.api_futures import APIFutures

app = Flask(__name__)

api_key = "039c26c7f5316ab9891ed924b3a4885bf35c70fe"
secret_key = "866cee39cb5a66816c815ee46481530f4d6b984bcf8eb9f9676715ee46fe2e37"
memo = "5"
url = "https://api-cloud.bitmart.com/futures/v1"
symbol = "XLM_USDT"
contract_type = "quarter"
api = APIFutures(api_key, secret_key, memo, url)

@app.route('/current_price')
def get_current_price():
    ticker = api.get_ticker(symbol, contract_type)
    return jsonify(ticker['last'])

@app.route('/moving_average')
def calculate_moving_average():
    kline = api.get_kline(symbol, contract_type, '1h', 20)
    close_prices = [float(price['close']) for price in kline]
    moving_average = talib.SMA(close_prices, timeperiod=20)
    return jsonify(moving_average[-1])

@app.route('/bollinger_bands')
def calculate_bollinger_bands():
    kline = api.get_kline(symbol, contract_type, '1h', 20)
    close_prices = [float(price['close']) for price in kline]
    upper_band, middle_band, lower_band = talib.BBANDS(close_prices, timeperiod=20)
    return jsonify(upper_band[-1], middle_band[-1], lower_band[-1])

def fibonacci_levels(start, end):
    levels = []
    level_0 = start
    level_1 = start
    level_2 = start + (end - start) * 0.236
    level_3 = start + (end - start) * 0.382
    level_4 = start + (end - start) * 0.5
    level_5 = start + (end - start) * 0.618
    level_6 = start + (end - start) * 0.764
    level_7 = end

    levels.extend([level_0, level_1, level_2, level_3, level_4, level_5, level_6, level_7])
    return levels

# Example usage
start_price = 100
end_price = 200
fib_levels = fibonacci_levels(start_price, end_price)
print(fib_levels)

@app.route('/buy_xlm/<price>')
def buy_xlm(price):
    api.create_order(symbol, contract_type, 'limit', 'buy', price, '1')
    return jsonify(message="Buy order placed")

@app.route('/sell_xlm/<price>')
def sell_xlm(price):
    api.create_order(symbol, contract_type, 'limit', 'sell', price, '1')
    return jsonify(message="Sell order placed")

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='127.0.0.1')