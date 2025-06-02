# 💰 Moneyy.AI

A trading analytics platform developed as part of an assignment to demonstrate REST API development, real-time data processing, and cloud integration with AWS.

---

## 📁 Project Structure

Moneyy.AI/
├── app/
│ ├── main.py # FastAPI entry point
│ ├── crud.py # CRUD operations
│ ├── database.py # DB connection setup
│ ├── models.py # Pydantic/ORM models
│ ├── schemas.py # Request/Response schemas
│ ├── tasks.py # Celery background tasks
│ ├── celery.py # Celery config
├── aws/
│ └── lambda_function.py # AWS Lambda to analyze S3 trade data
├── websocket_client.py # Client to consume real-time data
├── mock_websocket_Server.py # Mock WebSocket server (simulator)
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── .gitignore
├── venv/ # Python virtual environment


---

## 🚀 Features Completed (✅ Till Task 3)

### ✅ 1. REST API Development with FastAPI
- **Add Trade**: `POST /trades`
- **Fetch Trades**: `GET /trades?ticker=XYZ&from=DATE&to=DATE`
- **Database**: PostgreSQL (or MongoDB) connected via SQLAlchemy or async ORM
- **Validation**: Enforced using Pydantic models
- **Bonus**: Celery tasks for background notifications (e.g., stock threshold alerts)

### ✅ 2. Real-Time Data Processing via WebSocket
- **Client**: `websocket_client.py` simulates real-time data consumption
- **Monitoring**: Alerts on price increases > 2% within a minute
- **Bonus**: Calculates average price every 5 minutes and stores in DB

### ✅ 3. Cloud Integration with AWS Lambda
- **S3 Data Storage**: Trade data structured as `YEAR/MONTH/DATE/trades.csv`
- **Lambda Function**:
  - Fetches latest file by date
  - Calculates total traded volume & average price per stock
  - Writes back to `analysis_DATE.csv` in S3
- **Bonus**:
  - API Gateway to trigger Lambda with date parameter
  - Uses Boto3 for S3 operations

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/moneyy.ai.git
cd moneyy.ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

▶️ FastAPI Server
bash
Copy
Edit
uvicorn app.main:app --reload
▶️ Start Celery Worker
bash
Copy
Edit
celery -A app.celery worker --loglevel=info
▶️ WebSocket Client
bash
Copy
Edit
python websocket_client.py
☁️ AWS Lambda & S3
Create an S3 bucket and upload trade files.

Deploy aws/lambda_function.py as a Lambda function.

Use API Gateway or manual testing to trigger it with a date parameter.

Output is stored as analysis CSV in the same bucket path.

📦 Tech Stack
FastAPI for backend API

PostgreSQL / MongoDB for data storage

Celery + Redis for background tasks

WebSocket for real-time price tracking

AWS Lambda + S3 + Boto3 for cloud data processing

📄 License
MIT License — free to use, modify, and distribute.
