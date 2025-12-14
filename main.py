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

class LoginRequest(BaseModel):
    access_code: str

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

@app.post("/login")
def login(creds: LoginRequest):
    """Secure Access Protocol Verification"""
    # Environment variable support for security, default to 'nexus'
    SECRET_CODE = os.getenv("ACCESS_CODE", "nexus")
    
    if creds.access_code == SECRET_CODE:
        return {"status": "success", "token": "authorized_0x99"}
    else:
        return {"status": "failed", "message": "ACCESS DENIED"}

if __name__ == "__main__":
    print("🚀 Server starting! Open this link: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
