import boto3
import csv
import os
import json
from io import StringIO
from datetime import datetime
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        bucket = os.environ['BUCKET_NAME']
       

        # Parse JSON body from API Gateway event
        body = event.get("body")
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing request body"})
            }
        
        data = json.loads(body)
        date = data.get("date")
        date_obj = datetime.strptime(date, "%Y/%m/%d")

# format date to string without slashes for filename
        safe_date_str = date_obj.strftime("%Y%m%d")  # e.g., "20250601"
        if not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'date' in request"})
            }

        prefix = f"{date}/"  # e.g., "2025/06/01/"

        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        
        if 'Contents' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "No files found for given date"})
            }

        files = sorted([obj['Key'] for obj in response['Contents'] if 'trades.csv' in obj['Key']])
        
        if not files:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "No trades.csv file found for given date"})
            }

        latest_file = files[-1]
        obj = s3.get_object(Bucket=bucket, Key=latest_file)
        content = obj['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(content)

        summary = {}
        for row in reader:
            ticker = row['ticker']
            price = float(row['price'])
            qty = int(row['quantity'])
            if ticker not in summary:
                summary[ticker] = {"total_volume": 0, "total_value": 0}
            summary[ticker]["total_volume"] += qty
            summary[ticker]["total_value"] += price * qty

        for ticker in summary:
            vol = summary[ticker]["total_volume"]
            summary[ticker]["avg_price"] = summary[ticker]["total_value"] / vol

        # Save analysis
        out_key = f"{prefix}analysis_{safe_date_str}.csv"
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ticker", "total_volume", "avg_price"])
        for k, v in summary.items():
            writer.writerow([k, v["total_volume"], v["avg_price"]])

        s3.put_object(Bucket=bucket, Key=out_key, Body=output.getvalue())

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "success",
                "file": out_key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }


