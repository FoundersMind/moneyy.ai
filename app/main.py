from fastapi import FastAPI, BackgroundTasks, Query
from app.schemas import Trade, TradeQuery
from app.crud import add_trade, get_trades
from datetime import datetime
from app.tasks import notify_price_threshold

app = FastAPI()

@app.post("/trade")
async def create_trade(trade: Trade):
    trade.timestamp = trade.timestamp or datetime.utcnow()
    trade_dict = trade.dict()
    await add_trade(trade_dict)
    notify_price_threshold.delay(trade.ticker, trade.price)
    return {"message": "Trade recorded"}

@app.get("/trades")
async def fetch_trades(ticker: str = None, start: str = None, end: str = None):
    query = {}
    if ticker: query["ticker"] = ticker
    if start or end:
        query["timestamp"] = {}
        if start: query["timestamp"]["$gte"] = datetime.fromisoformat(start)
        if end: query["timestamp"]["$lte"] = datetime.fromisoformat(end)
    trades = await get_trades(query)
    return trades
