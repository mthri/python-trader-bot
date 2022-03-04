import time
import pandas as pd
import pandas_ta as ta
import ccxt


# + create exchange
# + if need to buy/sell
# `
# exchange = ccxt.binance({
#     "apiKey": API_KEY,
#     "secret": API_SECRET
# })
# `
exchange = ccxt.binance()

# get numbers of candle
def get_ohlcv(symbol, interval='1m', limit=10) -> pd.DataFrame:

    # headers
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

    # get candles from exchange
    bars = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=limit)

    # convert list of list to pandas dataframe
    df = pd.DataFrame(bars, columns=columns)

    # convert millisecond to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df

if __name__ == '__main__':
    symbol = 'BTC/USDT'
    quantity = 1.0
    dataframe = get_ohlcv(symbol, limit=50, interval='1m')

    # calculate last row index
    last_row = len(dataframe.index) - 1

    # calculate some indicator for fun :)
    dataframe['rsi3'] = ta.rsi(dataframe['close'], length=3)
    dataframe['sma3'] = ta.sma(dataframe['close'], length=3)
    
    macd = ta.macd(dataframe['close'], fast=12, slow=26, signal=9)
    dataframe['signal'] = ta.supertrend(dataframe['high'], dataframe['low'], 
                                        dataframe['close'], 8, 2)['SUPERTd_8_2.0']

    # print(dataframe)

    # very simple trader bot!
    print('bot is started!')
    bought = False
    while True:

        dataframe = get_ohlcv(symbol, limit=100)
        last_row = len(dataframe.index) - 2

        dataframe['signal'] = ta.supertrend(dataframe['high'], dataframe['low'], 
                                            dataframe['close'], 8, 2)['SUPERTd_8_2.0']

        current_price = dataframe['close'][last_row]
        current_time = dataframe['timestamp'][last_row]

        if not bought:
            if dataframe['signal'][last_row] == 1:
                print(f'buy signal for {symbol} on {current_price} at {current_time}')
                # exchange.create_market_buy_order(symbol, quantity)
                bought = True

        else:
            if dataframe['signal'][last_row] == -1:
                print(f'sell signal for {symbol} on {current_price} at {current_time}')
                # exchange.create_market_buy_order(symbol, quantity)
                bought = False
        
        time.sleep(60)





