from app.database import db
from datetime import datetime

async def add_trade(trade_data: dict):
    await db.trades.insert_one(trade_data)

async def get_trades(query: dict):
    cursor = db.trades.find(query)
    return await cursor.to_list(length=100)

# New function to save average price
from app.database import db
async def save_average_price(ticker: str, avg_price: float, timestamp):
    record = {
        "ticker": ticker,
        "average_price": avg_price,
        "timestamp": timestamp.isoformat()
    }
    print(f"Saving average price: {record}")
    try:
        result = await db.average_prices.update_one(
            {"ticker": ticker, "timestamp": record["timestamp"]},
            {"$set": record},
            upsert=True
        )
        print(f"MongoDB update_one result: matched={result.matched_count}, modified={result.modified_count}, upserted_id={result.upserted_id}")
    except Exception as e:
        print(f"Error saving average price: {e}")
