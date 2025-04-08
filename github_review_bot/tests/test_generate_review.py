"""
Tests for generate_review.py script.
"""

import pytest
from typing import Dict, Any, Tuple
from github_review_bot.scripts.generate_review import generate_review

def test_generate_review_interface():
    """Test the interface of generate_review function."""
    # Test missing required argument
    with pytest.raises(TypeError):
        generate_review()
    
    # Test wrong argument type
    with pytest.raises(TypeError):
        generate_review("not a dict")
    
    # Test correct usage
    mock_results = {
        'passed': True,
        'issues': [],
        'stats': {}
    }
    result = generate_review(mock_results)
    
    # Verify return type
    assert isinstance(result, tuple)
    assert len(result) == 2
    review_body, review_action = result
    assert isinstance(review_body, str)
    assert isinstance(review_action, str)
    assert review_action in ('approve', 'request_changes')

def test_generate_review_functionality():
    """Test the actual functionality of generate_review."""
    # Test passing case
    passing_results = {
        'passed': True,
        'issues': [],
        'stats': {}
    }
    review_body, review_action = generate_review(passing_results)
    assert "✅ All automated checks passed" in review_body
    assert review_action == 'approve'
    
    # Test failing case
    failing_results = {
        'passed': False,
        'issues': [{'tool': 'flake8', 'output': 'E501 line too long'}],
        'stats': {}
    }
    review_body, review_action = generate_review(failing_results)
    assert "⚠️ Some issues were found" in review_body
    assert review_action == 'request_changes' 