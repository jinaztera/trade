import ccxt
import pprint

# with open("../binance.key") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip()
#     api_secret = lines[1].strip()
   

api_key = "3o8od3V5ePVCnZ19u34KydThmSgbD2ekCV4yD9ZclRogzMvMl4RPFlfLW8fVpzFX"
api_secret = "ZRzqHcLKS7Lnemy5cwM2Cck0HRnguN59jQvzAqrrXAoZvGwS9AKZk1dHbvZqBXyA"

exchange = ccxt.binance(config={
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'       # 선물 거래
    }
})
print(exchange)

markets = exchange.load_markets()
tickers = exchange.fetch_tickers()

# :usdt 종목 선별
symbols = tickers.keys()
usdt_symbols = [x for x in symbols if x.endswith("USDT")]

import pandas as pd

timeframe = '1d'

# 각 코인의 가격 데이터를 저장할 딕셔너리
prices_data = {}

# 각 심볼에 대해 OHLCV 데이터를 가져와서 딕셔너리에 저장
for symbol in usdt_symbols[:5]:
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=2000)
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')  # timestamp를 datetime으로 변환
    
    if len(df) > 600:
        print(symbol)
        prices_data[symbol[:-10]] = df

# sym_lsit 종목 리스트 담기
sym_list = []
for key in prices_data.items():
    sym_list.append(key[0])