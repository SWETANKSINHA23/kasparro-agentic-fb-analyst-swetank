"""Test configuration loading"""
import os
import yaml
import pytest
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_load_config():
    """Test that configuration file loads successfully"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    
    # Check file exists
    assert os.path.exists(config_path), f"Config file not found: {config_path}"
    
    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check required keys (based on reference output)
    required_keys = ['project', 'data', 'thresholds', 'analysis', 'outputs', 'runtime']
    for key in required_keys:
        assert key in config, f"Missing required config key: {key}"
    
    # Print config info
    print(f"\nConfig keys: {list(config.keys())}")
    print(f"Dataset path: {config['data']['csv_path']}")
    print(f"Sample mode: {config['data'].get('sample_mode', False)}")
    
    assert True


if __name__ == "__main__":
    test_load_config()

# refactor later

# refactor later

# TODO: check this

# refactor later

# temporary fix

# optimized
