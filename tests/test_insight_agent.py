import pytest
import sys
import os
import yaml
import pandas as pd
from datetime import timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.insight_agent import InsightAgent
from src.agents.data_agent import DataAgent

def load_test_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def test_hypothesis_generation():
    """Test that Insight Agent generates hypotheses from data"""
    cfg = load_test_config()
    data_agent = DataAgent(cfg)
    insight_agent = InsightAgent(cfg)
    
    # Setup dates
    data_info = data_agent.get_data_info()
    end_date = pd.to_datetime(data_info['date_range']['end'])
    recent_start = (end_date - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    prev_start = (end_date - timedelta(days=14)).strftime('%Y-%m-%d')
    
    # Analyze
    insights = insight_agent.analyze(
        data_agent, 
        recent_start, 
        end_date_str, 
        prev_start, 
        recent_start
    )
    
    print("\n--- RECENT WINDOW ---")
    print(insights['recent_window'])
    
    print("\n--- PREVIOUS WINDOW ---")
    print(insights['previous_window'])
    
    print("\n--- PERCENT CHANGES ---")
    changes_print = {}
    for k, v in insights['changes'].items():
        new_k = k.replace('_change', '')
        changes_print[new_k] = v * 100 
    print(changes_print)
    
    print("\n--- HYPOTHESES ---")
    for h in insights['hypotheses']:
        print(f"- {h['hypothesis']}")

if __name__ == "__main__":
    test_hypothesis_generation()

# optimized

# optimized

# TODO: check this
