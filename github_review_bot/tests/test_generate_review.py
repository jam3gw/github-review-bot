"""
Tests for generate_review.py script.
"""

import os
import pytest
import shutil
from typing import Dict, Any, Tuple
from github_review_bot.scripts.generate_review import generate_review

@pytest.fixture(autouse=True)
def setup_config():
    """Setup test config before each test."""
    # Copy mock config to expected location
    src = "github_review_bot/tests/fixtures/bot_config.json"
    dst = "bot_config.json"
    shutil.copy(src, dst)
    yield
    # Clean up after test
    if os.path.exists(dst):
        os.remove(dst)

@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration for testing."""
    return {
        "repo_type": "default",
        "review_strictness": "medium",
        "enabled_checks": {
            "code_style": True,
            "security": True,
            "performance": True,
            "test_coverage": True,
            "documentation": True
        }
    }

def test_generate_review_interface(mock_config):
    """Test the interface of generate_review function."""
    # Test missing required arguments
    with pytest.raises(TypeError):
        generate_review()
    
    with pytest.raises(TypeError):
        generate_review({"passed": True})  # Missing config
    
    # Test wrong argument types
    with pytest.raises(TypeError):
        generate_review("not a dict", mock_config)
    
    with pytest.raises(TypeError):
        generate_review({"passed": True}, "not a dict")
    
    # Test correct usage
    mock_results = {
        'passed': True,
        'issues': [],
        'stats': {}
    }
    result = generate_review(mock_results, mock_config)
    
    # Verify return type
    assert isinstance(result, tuple)
    assert len(result) == 2
    review_body, review_action = result
    assert isinstance(review_body, str)
    assert isinstance(review_action, str)
    assert review_action in ('APPROVE', 'REQUEST_CHANGES')

def test_generate_review_functionality(mock_config):
    """Test the actual functionality of generate_review."""
    # Test passing case
    passing_results = {
        'passed': True,
        'issues': [],
        'stats': {}
    }
    review_body, review_action = generate_review(passing_results, mock_config)
    assert "✅ All automated checks passed" in review_body
    assert review_action == 'APPROVE'
    
    # Test failing case
    failing_results = {
        'passed': False,
        'issues': [{'tool': 'flake8', 'output': 'E501 line too long'}],
        'stats': {}
    }
    review_body, review_action = generate_review(failing_results, mock_config)
    assert "⚠️ Some issues were found" in review_body
    assert review_action == 'REQUEST_CHANGES' 