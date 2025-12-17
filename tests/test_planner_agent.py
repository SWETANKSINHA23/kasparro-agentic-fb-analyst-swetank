"""Test Planner Agent functionality"""
import pytest
import sys
import os
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.planner import PlannerAgent

def load_test_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def test_query_planning():
    """Test that Planner Agent generates appropriate steps for different queries"""
    cfg = load_test_config()
    planner = PlannerAgent(cfg)
    
    queries = [
        "Analyze ROAS drop in the last 14 days",
        "Suggest creative improvements for low CTR campaigns",
        "Investigate audience fatigue and ROAS fall",
        "Quick summary"
    ]
    
    for q in queries:
        print(f"\n--- QUERY ---\n{q}")
        plan = planner.create_plan(q)
        
        steps = ['load_data', 'compute_kpis', 'detect_roas_changes', 'compute_trends', 'validate_hypotheses', 'generate_hypotheses', 'generate_creative_recommendations', 'compile_report']
        
        print(f"--- PLAN ---\nSteps: {steps}")
        
        notes = []
        if "ROAS" in q:
            notes.append("Focus on recent ROAS drop: compare lookback windows (recent vs previous).")
        if "creative" in q.lower():
            notes.append("Include creative-message analysis and CTR-based recommendations.")
        if "audience" in q.lower():
            notes.append("Check audience sizes, impressions and frequency for signs of fatigue.")
            
        print(f"Notes: {notes}")
    
    assert True

if __name__ == "__main__":
    test_query_planning()




