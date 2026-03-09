"""
Working LangGraph state definition for the AI Analytics System
"""
from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field
import pandas as pd
from pydantic.config import ConfigDict
from langgraph.graph.message import add_messages, BaseMessage
from typing_extensions import TypedDict
from operator import add

# Use TypedDict with proper LangGraph annotations
class AnalyticsState(TypedDict):
    """State object for LangGraph workflow"""
    
    # Input - make question immutable after initialization
    question: str
    
    # Router outputs
    intent: Annotated[str, lambda x, y: y]
    needs_analysis: Annotated[bool, lambda x, y: y]
    needs_visualization: Annotated[bool, lambda x, y: y]
    
    # SQL generation with history
    sql_queries: Annotated[List[str], add]  # History of all SQL attempts
    current_sql: Annotated[str, lambda x, y: y]  # Current SQL to execute
    
    # SQL execution
    query_result: Optional[pd.DataFrame]
    
    # Retry logic
    retries_left: Annotated[int, lambda x, y: y]
    max_retries: int
    last_error: Annotated[str, lambda x, y: y]
    
    # Analysis outputs
    insights: Annotated[str, lambda x, y: y]
    chart_spec: Annotated[Dict[str, Any], lambda x, y: y]
    
    # Logging
    logs: List[str]
    
    # Messages for LangGraph
    messages: List[BaseMessage]

class StateHelper:
    """Helper class for state operations"""
    
    @staticmethod
    def add_log(state: AnalyticsState, message: str):
        """Add a log message with timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        # Simple append for logs
        current_logs = state.get("logs", [])
        current_logs.append(log_entry)
        state["logs"] = current_logs
    
    @staticmethod
    def get_table_preview(state: AnalyticsState) -> str:
        """Get markdown preview of query results"""
        if state.get("query_result") is None:
            return "No data available"
        return state["query_result"].head(20).to_markdown()
    
    @staticmethod
    def get_json_data(state: AnalyticsState) -> List[Dict[str, Any]]:
        """Get query results as JSON records"""
        if state.get("query_result") is None:
            return []
        return state["query_result"].to_dict('records')
    
    @staticmethod
    def initialize_state(question: str) -> AnalyticsState:
        """Initialize state with default values"""
        state = {
            "question": question,
            "intent": "",
            "needs_analysis": False,
            "needs_visualization": False,
            "sql_queries": [],  # Start with empty history
            "current_sql": "",
            "query_result": None,
            "retries_left": 4,  # Use retries_left instead of retry_count
            "max_retries": 4,
            "last_error": "",
            "insights": "",
            "chart_spec": {},
            "logs": [],
            "messages": []
        }
        return state
