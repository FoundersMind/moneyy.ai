import asyncio
import websockets
import json
from datetime import datetime, timedelta
from collections import defaultdict, deque

from app.crud import save_average_price  # your db saving logic here

# Constants
WS_URI = "ws://localhost:8067"  # Your mock server URI
PRICE_INCREASE_THRESHOLD = 0.02  # 2% increase threshold
PRICE_WINDOW = timedelta(minutes=1)  # 1-minute window for notifications
AVERAGE_INTERVAL = 10  

# Data structure to keep price history for each ticker
price_history = defaultdict(deque)  # {ticker: deque[(timestamp, price)]}

async def process_price_update(ticker, price, timestamp):
    prices = price_history[ticker]

    # Remove prices older than 1 minute from left of deque
    while prices and (timestamp - prices[0][0]) > PRICE_WINDOW:
        prices.popleft()

    # Check if price increased by >2% compared to oldest price in the 1-minute window
    if prices:
        old_price = prices[0][1]
        if old_price > 0 and (price - old_price) / old_price > PRICE_INCREASE_THRESHOLD:
            print(f"Notification: {ticker} price increased more than 2% in last minute!")

    # Append current price update
    prices.append((timestamp, price))
from datetime import datetime, timezone

async def calculate_average_prices():
    while True:
        await asyncio.sleep(AVERAGE_INTERVAL)
        now = datetime.now(timezone.utc)  # timezone-aware
        print(f"Calculating average prices at {now.isoformat()}")

        for ticker, prices in price_history.items():
            recent_prices = [p for t, p in prices if (now - t).total_seconds() <= AVERAGE_INTERVAL]

            if recent_prices:
                avg_price = sum(recent_prices) / len(recent_prices)
                await save_average_price(ticker, avg_price, now)

        print("Average prices saved to DB.")


async def listen_to_ws():
    async with websockets.connect(WS_URI) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            # Data example: {"ticker": "AAPL", "price": 150.23, "timestamp": "2025-06-01T12:34:56.123Z"}

            ticker = data.get("ticker")
            price = float(data.get("price"))
            timestamp = datetime.fromisoformat(data.get("timestamp").replace("Z", "+00:00"))

            await process_price_update(ticker, price, timestamp)

async def main():
    # Run listener and average price calculator concurrently
    await asyncio.gather(listen_to_ws(), calculate_average_prices())

if __name__ == "__main__":
    asyncio.run(main())
