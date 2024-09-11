from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from stock_data import get_stock_data, get_stock_general_info
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

stock_data = {
    "AAPL": [],
    "GOOGL": [2750.55, 2762.03, 2741.65, 2734.92, 2759.61],
    "AMZN": [3470.05, 3493.21, 3455.64, 3438.18, 3489.34],
}


# test http://127.0.0.1:8000/stock_prices/?stock_name=AAPL
@app.get("/stock_prices/", response_model=List[StockPrice])
def get_stock_prices(stock_name: str):
    """
    Retrieve the list of closing prices for a given stock name.

    :param stock_name: The name of the stock (e.g., AAPL, GOOGL).
    :return: A list of closing prices for the stock.
    """
    if stock_name in stock_data:
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
    if stock_name in stock_data:
        return get_stock_general_info(stock_name)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")

