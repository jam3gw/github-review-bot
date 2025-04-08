"""
Tests for load_config.py script.
"""

import pytest
from typing import Dict, Any
from github_review_bot.scripts.load_config import load_config, DEFAULT_CONFIG

def test_load_config_interface():
    """Test the interface of load_config function."""
    # Test with wrong argument type
    with pytest.raises(TypeError):
        load_config(123)  # type: ignore
    
    # Test with default argument
    result = load_config()
    assert isinstance(result, dict)
    
    # Test with explicit path
    result = load_config(".github/bot-config.yml")
    assert isinstance(result, dict)

def test_load_config_functionality():
    """Test the actual functionality of load_config."""
    # Test loading default config
    config = load_config("nonexistent.yml")
    assert config == DEFAULT_CONFIG
    
    # Test merging with user config
    # TODO: Add test with actual config file
    
    # Test config structure
    config = load_config()
    assert 'repo_type' in config
    assert 'review_strictness' in config
    assert 'enabled_checks' in config
    assert isinstance(config['enabled_checks'], dict) 