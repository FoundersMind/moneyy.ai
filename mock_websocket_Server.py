import asyncio
import websockets
import json
from datetime import datetime, timezone
import random

# List of sample tickers
TICKERS = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN"]

# Initialize prices for each ticker
prices = {ticker: 100 + random.uniform(-5, 5) for ticker in TICKERS}

async def send_price_updates(websocket):
    while True:
        # Simulate price updates
        for ticker in TICKERS:
            # Random walk price change within ±1%
            change_percent = random.uniform(-0.01, 0.01)
            prices[ticker] *= (1 + change_percent)
            prices[ticker] = round(prices[ticker], 2)

            message = {
                "ticker": ticker,
                "price": prices[ticker],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.1)  # short pause between each ticker

        await asyncio.sleep(1)  # wait 1 second before next batch

async def main():
    async with websockets.serve(send_price_updates, "localhost", 8067):
        print("Mock WebSocket server started on ws://localhost:8067")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
