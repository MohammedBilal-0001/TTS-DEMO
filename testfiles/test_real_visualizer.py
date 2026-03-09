#!/usr/bin/env python3
"""
Test visualizer with actual database data to see real visualization
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import AnalyticsState, StateHelper
from agents import visualizer_agent
import sqlite3
import pandas as pd

def get_real_data():
    """Get actual data from database"""
    conn = sqlite3.connect('../database/analytics.db')
    
    # Test different queries
    queries = [
        "SELECT region, SUM(revenue) as total_revenue FROM orders GROUP BY region",
        "SELECT product, AVG(revenue) as avg_revenue FROM orders GROUP BY product",
        "SELECT STRFTIME('%Y', order_date) as year, SUM(revenue) as total_revenue FROM orders GROUP BY STRFTIME('%Y', order_date)"
    ]
    
    test_data = []
    for query in queries:
        try:
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                test_data.append((query, df))
                print(f"Query: {query}")
                print(f"Data shape: {df.shape}")
                print(f"Sample data:\n{df.head()}\n")
        except Exception as e:
            print(f"Error with query '{query}': {e}")
    
    conn.close()
    return test_data

# Test different questions with real data
test_questions = [
    "Show total revenue by region",
    "Show average revenue by product", 
    "Show revenue trends over time"
]

print("=== Testing Visualizer with Real Database Data ===\n")

# Get real data
real_data_samples = get_real_data()

if not real_data_samples:
    print("No data found in database. Please run database setup first.")
    sys.exit(1)

# Test with real data
for i, (query, data) in enumerate(real_data_samples):
    if i < len(test_questions):
        question = test_questions[i]
        print(f"Question: {question}")
        print(f"Using data from query: {query}")
        
        # Create state with question and real data
        state = StateHelper.initialize_state(question)
        state["query_result"] = data
        state["question"] = question
        
        # Run visualizer
        result = visualizer_agent(state)
        chart_spec = result["chart_spec"]
        
        print(f"Chart Type: {chart_spec.get('chart_type')}")
        print(f"X-axis: {chart_spec.get('x')}")
        print(f"Y-axis: {chart_spec.get('y')}")
        print(f"Title: {chart_spec.get('title')}")
        print(f"Actual data values: {data.to_dict('records')[:3]}")  # Show first 3 rows
        print("-" * 50)
