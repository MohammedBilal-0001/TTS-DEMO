"""
SQL executor tool with safety checks
"""
import sqlite3
import pandas as pd
import os
from typing import Optional, List
from state import AnalyticsState, StateHelper

# Unsafe SQL keywords that should be blocked
UNSAFE_KEYWORDS = [
    'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 
    'TRUNCATE', 'EXEC', 'EXECUTE', 'MERGE'
]

def is_safe_sql(sql_query: str) -> tuple[bool, str]:
    """Check if SQL query is safe to execute"""
    
    if not sql_query.strip():
        return False, "Empty SQL query"
    
    # Convert to uppercase for checking
    sql_upper = sql_query.upper()
    
    # Check for unsafe keywords
    for keyword in UNSAFE_KEYWORDS:
        if keyword in sql_upper:
            return False, f"Unsafe keyword detected: {keyword}"
    
    # Allow SELECT statements and JOINs (be more flexible)
    sql_clean = sql_upper.strip()
    # Remove any leading characters that might be artifacts
    while sql_clean and not sql_clean.startswith('SELECT'):
        if sql_clean.startswith('SELECT'):
            break
        # Remove first character and check again
        sql_clean = sql_clean[1:].strip()
    
    if not sql_clean.startswith('SELECT'):
        return False, "Only SELECT queries are allowed"
    
    # Allow JOIN, INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN
    # These are safe for read-only operations
    
    return True, "Query is safe"

def execute_sql_tool(state: AnalyticsState) -> AnalyticsState:
    """Execute SQL query against SQLite database"""
    
    StateHelper.add_log(state, "SQL Executor: Preparing to execute query")
    print(f"[SQL Executor] Preparing to execute query")
    print(f"[SQL Executor] Query: {state['current_sql']}")
    StateHelper.add_log(state, f"SQL Executor: Query: {state['current_sql']}")
    
    # Validate SQL
    is_safe, safety_message = is_safe_sql(state["current_sql"])
    
    if not is_safe:
        state["last_error"] = safety_message
        print(f"[SQL Executor] Safety check failed: {safety_message}")
        StateHelper.add_log(state, f"SQL Executor: Safety check failed - {safety_message}")
        return state
    
    try:
        # Connect to database using environment variable
        database_url = os.getenv('DATABASE_URL', 'sqlite:///C:/Users/USER/Desktop/Projects/Text-to-SQL-orc/database/analytics.db')
        # Extract path from sqlite:/// format
        if database_url.startswith('sqlite:///'):
            db_path = database_url[10:]  # Remove 'sqlite:///'
        else:
            db_path = database_url
        
        # Clean the SQL query - remove any leading artifacts
        sql_clean = state["current_sql"].strip()
        while sql_clean and not sql_clean.upper().startswith('SELECT'):
            if sql_clean.upper().startswith('SELECT'):
                break
            sql_clean = sql_clean[1:].strip()
        
        print(f"[SQL Executor] Cleaned query: {sql_clean}")
        state["current_sql"] = sql_clean  # Update with cleaned query
            
        conn = sqlite3.connect(db_path)
        
        # Execute query and get results
        state["query_result"] = pd.read_sql_query(state["current_sql"], conn)
        
        # Close connection
        conn.close()
        
        # Clear any previous errors
        state["last_error"] = ""
        
        print(f"[SQL Executor] Query executed successfully ({len(state['query_result'])} rows)")
        StateHelper.add_log(state, f"SQL Executor: Query executed successfully ({len(state['query_result'])} rows)")
        
    except Exception as e:
        # Capture error
        state["last_error"] = str(e)
        state["query_result"] = None
        state["retries_left"] -= 1  # Decrease retries left
        
        print(f"[SQL Executor] Query failed: {str(e)}")
        print(f"[SQL Executor] Retries left: {state['retries_left']}")
        StateHelper.add_log(state, f"SQL Executor: Query failed - {str(e)}")
        StateHelper.add_log(state, f"SQL Executor: Retries left: {state['retries_left']}")
    
    return state

def retry_router(state: AnalyticsState) -> str:
    """Determine if SQL execution should be retried"""
    
    StateHelper.add_log(state, "Retry Router: Evaluating retry logic")
    
    if state["last_error"] and state["retries_left"] > 0:
        StateHelper.add_log(state, "Retry Router: Will retry SQL generation")
        return "retry"
    elif state["last_error"]:
        StateHelper.add_log(state, "Retry Router: Max retries exceeded")
        return "fail"
    else:
        StateHelper.add_log(state, "Retry Router: Query successful")
        return "success"

def intent_router(state: AnalyticsState) -> str:
    """Route based on the intent determined by the router agent"""
    
    StateHelper.add_log(state, f"Intent Router: Processing intent - {state.get('intent', 'unknown')}")
    
    intent = state.get("intent", "database_query")
    
    if intent == "general_question":
        StateHelper.add_log(state, "Intent Router: General question detected - skipping SQL")
        return "response_builder"
    elif intent == "other" or intent == "error":
        StateHelper.add_log(state, "Intent Router: Other/error intent - skipping SQL")
        return "response_builder"
    else:  # database_query
        StateHelper.add_log(state, "Intent Router: Database query detected - proceeding with SQL")
        return "text_to_sql"

def parallel_router(state: AnalyticsState) -> List[str]:
    """Determine which parallel agents should run"""
    
    StateHelper.add_log(state, "Parallel Router: Determining parallel execution")
    
    next_nodes = []
    
    if state["needs_analysis"]:
        next_nodes.append("analyzer")
        StateHelper.add_log(state, "Parallel Router: Will run analyzer")
    
    if state["needs_visualization"]:
        next_nodes.append("visualizer") 
        StateHelper.add_log(state, "Parallel Router: Will run visualizer")
    
    if not next_nodes:
        StateHelper.add_log(state, "Parallel Router: No parallel agents needed")
        next_nodes = ["response_builder"]
    
    return next_nodes
