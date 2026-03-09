#!/usr/bin/env python3
"""
Test workflow directly to debug the hanging issue
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import AnalyticsState, StateHelper
from workflow import compiled_workflow

# Test the workflow directly
print("Testing workflow directly...")
state = StateHelper.initialize_state('Show total revenue by region')
print("Initial state created")

try:
    print("Running workflow...")
    result = compiled_workflow.invoke(state)
    print("Workflow completed successfully!")
    print("Result keys:", list(result.keys()))
    print("Intent:", result.get('intent'))
    print("Logs:", result.get('logs', [])[:5])  # First 5 logs
except Exception as e:
    print(f"Workflow failed: {e}")
    import traceback
    traceback.print_exc()
