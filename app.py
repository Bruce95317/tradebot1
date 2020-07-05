from chalice import Chalice
import requests
import json

app = Chalice(app_name='tradebot-mac')

API_KEY = 'MyAPIkey'
SECRET_KEY = 'MyAPISecretkey'
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}


@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    request = app.current_request
    webhook_message = request.json_body

    data = {
        "symbol": webhook_message['ticker'],
        "qty": 1,
        "side": "buy",
        "type": "limit",
        "limit_price": webhook_message['close'],
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": webhook_message['close'] * 1.20
        },
        "stop_loss": {
            "stop_price": webhook_message['close'] * 0.90,
        }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

  
     try:
        response = json.loads(r.content)
        print(response)
        
    except Exception as e: 
        print(e)

    return {
        'webhook_message': webhook_message,
    }
