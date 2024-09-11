import yfinance as yf


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


# tickers = yf.Tickers('msft aapl goog')
#
# a = tickers.tickers['MSFT'].info  # here Open, High, Low, Close, Volume, Dividends, Stock Splits
# # for stock data we use the close value
# b = tickers.tickers['AAPL'].history(period="1mo")
# c = tickers.tickers['GOOG'].actions
# # data = yf.download("SPY AAPL", period="1mo")
#
get_stock_general_info("AAPL")
# # print(a, b, c)
