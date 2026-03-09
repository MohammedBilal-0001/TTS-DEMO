#!/usr/bin/env python3
"""
Test visualizer with different questions to see if it adapts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import AnalyticsState, StateHelper
from agents import visualizer_agent
import pandas as pd

# Create sample data like what the SQL executor would return
sample_data = pd.DataFrame({
    'region': ['North', 'South', 'East', 'West'],
    'total_revenue': [15000.0, 12000.0, 18000.0, 9000.0]
})

# Test different questions
test_questions = [
    "Show total revenue by region",
    "Show revenue trends over time", 
    "Which region has the highest sales?",
    "What percentage of sales comes from each region?"
]

print("=== Testing Visualizer with Different Questions ===\n")

for question in test_questions:
    print(f"Question: {question}")
    
    # Create state with question and data
    state = StateHelper.initialize_state(question)
    state["query_result"] = sample_data
    state["question"] = question
    
    # Run visualizer
    result = visualizer_agent(state)
    chart_spec = result["chart_spec"]
    
    print(f"Chart Type: {chart_spec.get('chart_type')}")
    print(f"X-axis: {chart_spec.get('x')}")
    print(f"Y-axis: {chart_spec.get('y')}")
    print(f"Title: {chart_spec.get('title')}")
    print("-" * 50)
