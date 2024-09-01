import yfinance as yf


def get_stock_price(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    if not data.empty:
        return round(data['Close'].iloc[0], 2)
    return None


tickers = yf.Tickers('msft aapl goog')

a = tickers.tickers['MSFT'].info  # here Open, High, Low, Close, Volume, Dividends, Stock Splits
# for stock data we use the close value
b = tickers.tickers['AAPL'].history(period="1mo")
c = tickers.tickers['GOOG'].actions
# data = yf.download("SPY AAPL", period="1mo")

# print(get_stock_price("AAPL"))
# print(a, b, c)
