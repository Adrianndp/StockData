import yfinance as yf
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


# Stock-related functions
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
    data = stock.history(period="3mo")
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


def get_current_price_data(ticker: any):
    temp = {
        'name': ticker.info['shortName'],
        'symbol': ticker.info['symbol'],
    }
    if ticker.info['quoteType'] == 'CRYPTOCURRENCY':
        temp['price'] = get_coingecko_price(ticker.info['name'].lower())
    elif ticker.info['quoteType'] == 'INDEX':
        temp['price'] = ticker.history(period="1d")['Close'].iloc[0]
    else:
        temp['price'] = ticker.info['currentPrice']
    previous_close = ticker.info['previousClose']
    temp['change'] = temp['price'] - previous_close
    temp['currency'] = ticker.info['currency']
    temp['percentage_change'] = (temp['change'] / previous_close) * 100
    temp['image_name'] = ticker.info['symbol'].lower() + ".svg"
    return temp


def get_top_stocks():
    tickers = yf.Tickers('AAPL GOOGL AMZN NFLX TSLA NKE MSFT META')
    data = tickers.tickers
    output = {}
    for ticker in data:
        temp = get_current_price_data(data[ticker])
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
        clean_data.append({
            'title': new['title'],
            'url': new['link'],
            'image_url': image_url
        })
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


# FastAPI application setup
class StockPrice(BaseModel):
    x: int  # Timestamp in milliseconds
    y: List[float]  # List of float values


class StockNews(BaseModel):
    title: str
    url: str
    image_url: Optional[str]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stock_prices/", response_model=List[StockPrice])
def get_stock_prices_request(stock_name: str):
    if stock_exists(stock_name):
        return get_stock_prices(stock_name)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")


@app.get("/stock_info/", response_model=Dict[str, Any])
def get_stock_info_request(stock_name: str):
    if stock_exists(stock_name):
        return get_stock_info(stock_name)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")


@app.get("/top_stocks/", response_model=Dict[str, Dict])
def get_top_stocks_request():
    return get_top_stocks()


@app.get("/stock_news/", response_model=List[StockNews])
def get_stock_news_request(stock_name: str):
    if stock_exists(stock_name):
        return get_stock_news(stock_name)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")


@app.get("/stock_current_price_data/", response_model=Dict[str, Any])
def get_current_price_data_request(stock_name: str):
    stock = yf.Ticker(stock_name)
    return get_current_price_data(stock)
