from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import logging

# Import database and agent logic
from app.database import get_db
from app.executor import run_agentic_query, run_mini_sql_agent

# Import your routers
from .routers import (
    product_router,
    productline_router,
    office_router,
    employee_router,
    order_router,
    orderdetail_router,
    payment_router
)

# Initialize logging before the app starts
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

# Initialize ONE FastAPI instance
app = FastAPI(title="ClassicModels Agentic Text-to-SQL API")
from pydantic import BaseModel

# This tells FastAPI what the JSON input should look like
class AgentRequest(BaseModel):
    question: str

# endpoint to use this model
@app.post("/agent/sql", tags=["Task 4"])
async def task_4_agent(payload: AgentRequest, db: Session = Depends(get_db)):
    # access the question :
    user_question = payload.question
    
    # agent logic
    response = run_mini_sql_agent(user_question, db)
    return response

# @app.post("/agent/sql", tags=["Task 4: Mini SQL Agent"])
# async def task_4_agent(payload: dict, db: Session = Depends(get_db)):
#     """
#     Task 4 specific endpoint.
#     Expects JSON: {"question": "How many shipped orders are from USA customers?"}
#     """
#     question = payload.get("question")
#     if not question:
#         raise HTTPException(status_code=400, detail="No question provided in payload")

#     # This calls the upgraded 3-retry logic
#     response = run_mini_sql_agent(question, db)
    
#     return response

# --- Agentic Text-to-SQL Endpoint ---
@app.post("/agent/query", tags=["AI Agent"])
async def agent_query(
    question: str = Query(..., description="Ask a question in plain English", example="List all products"), 
    db: Session = Depends(get_db)
):
    """
    Main entry point for the Text-to-SQL Agent.
    It performs: Decomposition -> SQL Generation -> Validation -> Execution -> Retry (if needed).
    """
    logger.info(f"Received agent question: {question}")
    
    # run_agentic_query handles the logic from Task 3 internally
    response = run_agentic_query(question, db)
    
    if response.get("status") == "error":
        # Return a 400 if the agent couldn't solve it, but keep the SQL for debugging
        return {
            "status": "error",
            "message": response.get("message"),
            "attempted_sql": response.get("sql")
        }
        
    return {
        "question": question,
        "sql": response.get("sql"),
        "result": response.get("result"),
        "status": "success",
        "retry_used": response.get("retry", False)
    }

# --- Standard CRUD Routers ---
app.include_router(product_router.router, prefix="/products", tags=["Products"])
app.include_router(productline_router.router, prefix="/productlines", tags=["ProductLines"])
app.include_router(office_router.router, prefix="/offices", tags=["Offices"])
app.include_router(employee_router.router, prefix="/employees", tags=["Employees"])
app.include_router(order_router.router, prefix="/orders", tags=["Orders"])
app.include_router(orderdetail_router.router, prefix="/orderdetails", tags=["OrderDetails"])
app.include_router(payment_router.router, prefix="/payments", tags=["Payments"])

@app.get("/", tags=["General"])
def root():
    return {"message": "ClassicModels AI Agent API is running!"}