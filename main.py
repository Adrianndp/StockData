from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from stock_data import get_stock_prices, get_stock_info, stock_exists, get_top_stocks, get_stock_news
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


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
