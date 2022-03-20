# for more details see here: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams

import pandas as pd
import pandas_ta as ta
import ccxt
from websocket import WebSocketApp

symbol = 'btcusdt'
interval = '1m'

'''
wss: protocol
stream.binance.com: host
9443: port
ws/symbol@kline_interval: path
'''
url =f'wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}'


# for more details about `websocket-client` see https://websocket-client.readthedocs.io/en/latest/examples.html
def websocket_on_open(ws: WebSocketApp, *args, **kwargs):
    print('websocket opened')

def websocket_on_close(ws: WebSocketApp, *args, **kwargs):
    print('websocket closed')

# important!, when server send any data, you got it here (means you can process it!)
def websocket_on_message(ws: WebSocketApp, message: str, *args, **kwargs):
    print('new message -> ', message)

# create websocket object
ws = WebSocketApp(url, on_open=websocket_on_open, 
                  on_close=websocket_on_close,
                  on_message=websocket_on_message)

# connect to server then run! easy peasy lemon squeezy :)))
ws.run_forever()
