from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from stock_data import get_stock_data, get_stock_general_info, stock_exists, get_top_stocks
from typing import List, Dict, Any
from pydantic import BaseModel


class StockPrice(BaseModel):
    x: int  # Timestamp in milliseconds
    y: List[float]  # List of float values


logging.basicConfig(level=logging.INFO)

# from enum import Enum
# from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# test http://127.0.0.1:8000/stock_prices/?stock_name=AAPL
@app.get("/stock_prices/", response_model=List[StockPrice])
def get_stock_prices(stock_name: str):
    """
    Retrieve the list of closing prices for a given stock name.

    :param stock_name: The name of the stock (e.g., AAPL, GOOGL).
    :return: A list of closing prices for the stock.
    """
    if stock_exists(stock_name):
        return get_stock_data(stock_name)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")


@app.get("/stock_info/", response_model=Dict[str, Any])
def get_stock_info(stock_name: str):
    """
    Retrieve the list of closing prices for a given stock name.

    :param stock_name: The name of the stock (e.g., AAPL, GOOGL).
    :return: A list of closing prices for the stock.
    """
    if stock_exists(stock_name):
        return get_stock_general_info(stock_name)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")


@app.get("/top_stocks/", response_model=Dict[str, Dict])
def get_top_stocks():
    return get_top_stocks()
