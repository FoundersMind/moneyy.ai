from .celery import celery_app

@celery_app.task
def notify_price_threshold(ticker, price):
    print(f"Notify: {ticker} crossed threshold with price {price}")
