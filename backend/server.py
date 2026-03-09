"""
FastAPI server for the AI Analytics System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from state import AnalyticsState, StateHelper
from workflow import compiled_workflow

# Initialize FastAPI app
app = FastAPI(title="AI Analytics System", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    insights: str
    chart_spec: Dict[str, Any]
    query_results: Dict[str, Any] = {}  # Add query results
    logs: List[str]
    success: bool
    error: str = ""

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Analytics System is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "llm": "configured",
        "workflow": "ready"
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query through the AI workflow"""
    
    try:
        # Initialize state properly
        state = StateHelper.initialize_state(request.question)
        
        # Run workflow
        result = compiled_workflow.invoke(state)
        
        # Prepare response
        query_results = {}
        if result.get("query_result") is not None:
            query_results = {
                "data": StateHelper.get_json_data(result),
                "columns": result["query_result"].columns.tolist() if hasattr(result["query_result"], 'columns') else []
            }
        
        response = QueryResponse(
            insights=result.get("insights", ""),
            chart_spec=result.get("chart_spec", {}),
            query_results=query_results,
            logs=result.get("logs", []),
            success=not bool(result.get("last_error", "")),
            error=result.get("last_error", "")
        )
        
        return response
        
    except Exception as e:
        # Log the error
        print(f"Error processing query: {str(e)}")
        
        # Return error response
        return QueryResponse(
            insights="",
            chart_spec={},
            query_results={},
            logs=[f"System error: {str(e)}"],
            success=False,
            error=str(e)
        )

@app.get("/demo-questions")
async def get_demo_questions():
    """Get list of demo questions for testing"""
    return {
        "questions": [
            "Show total revenue by region",
            "Which product generates the most revenue?",
            "Show revenue trends over time",
            "Which region has the lowest sales?",
            "What are the top 3 products by revenue?",
            "How many orders were placed in each region?",
            "What is the average order value?",
            "Show customer distribution by region"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    
    print(f"Starting AI Analytics System on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
