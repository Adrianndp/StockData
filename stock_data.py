import yfinance as yf


def stock_exists(symbol):
    ticker = yf.Ticker(symbol)
    try:
        stock_info = ticker.info
        return True if 'symbol' in stock_info else False
    except Exception as e:
        print(e)
        return False


def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")
    if not data.empty:
        data = data.to_dict('index')
        return [
            {
                'x': int(timestamp.to_pydatetime().timestamp() * 1000),
                'y': [values['Open'], values['High'], values['Low'], values['Close']]
            }
            for timestamp, values in data.items()
        ]
    return None


def get_stock_general_info(symbol: str):
    stock = yf.Ticker(symbol)
    return stock.info


def get_top_stocks():
    tickers = yf.Tickers('AAPL GOOGL AMZN NFLX ^GSPC TSLA NKE MSFT META BTC-USD ETH-USD ADA-USD DOGE-USD')
    data = tickers.tickers

    return [{
        'name': data[ticker].info['shortName'],
        'symbol': data[ticker].info['symbol'],
    } for ticker in data]


def get_stock_news(symbol: str):
    stock = yf.Ticker(symbol)
    return stock.news

# s = yf.Ticker("AAPL")
# print(s.fast_info.get('lastPrice'))
# print(get_stock_general_info("^GSPC"))
# print(get_top_stocks())
