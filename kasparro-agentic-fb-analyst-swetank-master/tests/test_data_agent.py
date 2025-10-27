"""Test Data Agent functionality"""
import pytest
import sys
import os
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.data_agent import DataAgent

def load_test_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def test_data_loading():
    """Test that Data Agent loads data successfully"""
    cfg = load_test_config()
    agent = DataAgent(cfg)
    df = agent.get_data()
    
    # Print summary
    print("\n--- DATA SUMMARY ---")
    
    info = agent.get_data_info()
    
    summary = {
        'dataset_info': {
            'rows': len(df),
            'columns': list(df.columns)
        },
        'missing_values': df.isnull().sum().to_dict(),
        'basic_stats': df.describe(include='all').to_dict()
    }
    
    print(summary)

if __name__ == "__main__":
    test_data_loading()

# optimized
