"""
Simplified LangGraph state definition for the AI Analytics System
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import pandas as pd
from pydantic.config import ConfigDict

class AnalyticsState(BaseModel):
    """State object for LangGraph workflow"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # Input
    question: str = Field(description="Original user question")
    
    # Router outputs
    intent: str = Field(default="", description="Type of request (e.g., 'database_query')")
    needs_analysis: bool = Field(default=False, description="Whether analysis is needed")
    needs_visualization: bool = Field(default=False, description="Whether visualization is needed")
    
    # SQL generation
    sql_query: str = Field(default="", description="Generated SQL query")
    
    # SQL execution
    query_result: Optional[pd.DataFrame] = Field(default=None, description="Results from SQL execution")
    
    # Retry logic
    retry_count: int = Field(default=0, description="Current retry number")
    max_retries: int = Field(default=4, description="Maximum retries allowed")
    last_error: str = Field(default="", description="Error message from failed SQL")
    
    # Analysis outputs
    insights: str = Field(default="", description="Analysis output")
    chart_spec: Dict[str, Any] = Field(default_factory=dict, description="Visualization instructions")
    
    # Logging
    logs: List[str] = Field(default_factory=list, description="Execution log messages")
    
    def add_log(self, message: str):
        """Add a log message with timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
    
    def get_table_preview(self) -> str:
        """Get markdown preview of query results"""
        if self.query_result is None:
            return "No data available"
        return self.query_result.head(20).to_markdown()
    
    def get_json_data(self) -> List[Dict[str, Any]]:
        """Get query results as JSON records"""
        if self.query_result is None:
            return []
        return self.query_result.to_dict('records')
