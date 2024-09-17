import yfinance as yf
import requests


def stock_exists(symbol):
    ticker = yf.Ticker(symbol)
    try:
        stock_info = ticker.info
        return True if 'symbol' in stock_info else False
    except Exception as e:
        print(e)
        return False


def get_stock_prices(symbol: str):
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


def get_stock_info(symbol: str):
    stock = yf.Ticker(symbol)
    return stock.info


def get_top_stocks():
    tickers = yf.Tickers('AAPL GOOGL AMZN NFLX ^GSPC TSLA NKE MSFT META BTC-USD')
    data = tickers.tickers
    output = {}
    for ticker in data:
        temp = {'name': data[ticker].info['shortName'],
                'symbol': data[ticker].info['symbol'],
                }
        if data[ticker].info['quoteType'] == 'CRYPTOCURRENCY':
            temp['price'] = get_coingecko_price(data[ticker].info['name'].lower())
        elif data[ticker].info['quoteType'] == 'INDEX':
            temp['price'] = data[ticker].history(period="1d")['Close'].iloc[0]
        else:
            temp['price'] = data[ticker].info['currentPrice']
        previous_close = data[ticker].info['previousClose']
        temp['change'] = temp['price'] - previous_close
        temp['percentage_change'] = (temp['change'] / previous_close) * 100
        temp['image_name'] = data[ticker].info['symbol'].lower() + ".svg"
        output[data[ticker].info['symbol']] = temp

    return output


def get_stock_news(symbol: str):
    stock = yf.Ticker(symbol)
    news = stock.news
    clean_data = []
    for new in news:
        if 'thumbnail' in new and 'resolutions' in new['thumbnail']:
            image_url = next((thumb['url'] for thumb in new['thumbnail']['resolutions'] if thumb['width'] == 140), None)
        else:
            image_url = None
        clean_data.append({'title': new['title'], 'url': new['link'], 'image_url': image_url})
    return clean_data


def get_coingecko_price(ticker):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd'
    response = requests.get(url)
    if response.status_code == 429:  # Too many requests
        print("Rate limit exceeded. Waiting for 60 seconds.")
    data = response.json()
    try:
        return data[ticker]['usd']
    except KeyError:
        return
