from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from categorizer import Categorizer
import database
import uvicorn
import os

# 1. Initialize App & DB
app = FastAPI(title="MLH Finance Tracker API")
database.init_db() # Create table on startup

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

categorizer = Categorizer()

# 2. Models
class TransactionRequest(BaseModel):
    description: str
    amount: float

class CategoryResponse(BaseModel):
    category: str
    confidence: str = "High"

# 3. Endpoints

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico") if os.path.exists("favicon.ico") else {"status": "ok"}

@app.post("/categorize", response_model=CategoryResponse)
def categorize_transaction(transaction: TransactionRequest):
    # 1. Categorize
    category_name = categorizer.categorize(transaction.description)
    
    # 2. Save to DB (Persistence!)
    database.add_transaction(transaction.description, transaction.amount, category_name)
    
    return CategoryResponse(category=category_name)

@app.get("/history")
def get_history():
    """Returns recent transactions (Limit 5 for dashboard)."""
    return database.get_recent_transactions(limit=5)

@app.get("/ledger")
def get_ledger():
    """Returns ALL transactions for the full ledger view."""
    return database.get_all_transactions()

@app.get("/analytics-data")
def get_analytics_data():
    """Returns daily spending trend."""
    return database.get_daily_spending()

@app.get("/summary")
def get_summary():
    """Returns spending breakdown for the chart."""
    return database.get_category_summary()

@app.post("/send-report")
def send_report():
    """Simulates sending an email report."""
    # In a real app, you would use smtplib here with os.getenv("SMTP_PASSWORD")
    summary = database.get_category_summary()
    total = sum(summary.values())
    
    print(f"📧 SENDING EMAIL TO USER: 'Your Total Spending: ${total:.2f}'")
    return {"status": "sent", "message": f"Report sent! Total spend: ${total:.2f}"}

if __name__ == "__main__":
    print("🚀 Server starting! Open this link: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
