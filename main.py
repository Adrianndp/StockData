from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging

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
    "AAPL": [150.75, 152.35, 149.85, 148.97, 151.83],
    "GOOGL": [2750.55, 2762.03, 2741.65, 2734.92, 2759.61],
    "AMZN": [3470.05, 3493.21, 3455.64, 3438.18, 3489.34],
}


# test http://127.0.0.1:8000/stock_prices/?stock_name=AAPL
@app.get("/stock_prices/", response_model=List[float])
def get_stock_prices(stock_name: str):
    """
    Retrieve the list of closing prices for a given stock name.

    :param stock_name: The name of the stock (e.g., AAPL, GOOGL).
    :return: A list of closing prices for the stock.
    """
    if stock_name in stock_data:
        logging.info("returning stock data")
        return stock_data[stock_name]
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
