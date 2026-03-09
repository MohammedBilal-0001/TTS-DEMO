#!/usr/bin/env python3
"""
Test script to verify the router fix for conversational questions
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from state import AnalyticsState
from agents import router_agent, response_builder_agent

def test_conversational_routing():
    """Test that conversational questions are routed correctly"""
    
    # Test cases
    test_questions = [
        "how are u today?",
        "hello there",
        "thanks for your help",
        "what's the weather like?",
        "show me sales data"  # This should still be a database query
    ]
    
    for question in test_questions:
        print(f"\n{'='*50}")
        print(f"Testing question: '{question}'")
        print(f"{'='*50}")
        
        # Create state
        state = AnalyticsState(question=question)
        
        # Test router
        router_result = router_agent(state)
        print(f"Router result: {router_result}")
        
        # Update state with router results
        state.update(router_result)
        
        # Test response builder
        response_result = response_builder_agent(state)
        print(f"Response: {response_result['insights']}")
        print(f"Chart type: {response_result['chart_spec']['chart_type']}")

if __name__ == "__main__":
    test_conversational_routing()
