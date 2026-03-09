#!/usr/bin/env python3
"""
Simple test to show logs from SQL execution
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import AnalyticsState, StateHelper
from agents import text_to_sql_agent
from tools import execute_sql_tool

# Test just the SQL generation and execution
print("=== Testing SQL Generation ===")
state = StateHelper.initialize_state('Show total revenue by region')
print("Initial state created")

# Test SQL generation
print("\n=== SQL Generation ===")
state = text_to_sql_agent(state)
print(f"Generated SQL: {state['sql_query']}")
print(f"Logs so far: {state['logs']}")

# Test SQL execution
print("\n=== SQL Execution ===")
state = execute_sql_tool(state)
print(f"Query result: {state['query_result']}")
print(f"Last error: {state['last_error']}")
print(f"Retry count: {state['retry_count']}")

print("\n=== All Logs ===")
for i, log in enumerate(state['logs']):
    print(f"{i+1}. {log}")
