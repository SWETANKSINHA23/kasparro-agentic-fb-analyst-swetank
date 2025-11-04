"""Test Creative Agent functionality"""
import pytest
import sys
import os
import yaml

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.creative_generator import CreativeGenerator
from src.agents.data_agent import DataAgent

def load_test_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def test_creative_generation():
    """Test that Creative Agent generates recommendations"""
    cfg = load_test_config()
    data_agent = DataAgent(cfg)
    creative_gen = CreativeGenerator(data_agent, cfg)
    
    recs = creative_gen.generate_creatives(min_spend=100.0) 
    
    print("\n--- GENERATED CREATIVE RECOMMENDATIONS ---")
    
    count = 1
    for r in recs:
        for msg in r.get('recommended_messages', []):
            print(f"{count}. {msg}")
            count += 1
            
    print("\nSaved creatives to reports/creatives.json")
    
    assert True


if __name__ == "__main__":
    test_creative_generation()

# optimized

# temporary fix

# optimized
