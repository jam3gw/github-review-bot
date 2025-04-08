"""
Tests for parse_review_preference.py script.
"""

import pytest
from typing import Literal
from github_review_bot.scripts.parse_review_preference import parse_review_preference

def test_parse_review_preference_interface():
    """Test the interface of parse_review_preference function."""
    # Test missing required argument
    with pytest.raises(TypeError):
        parse_review_preference()
    
    # Test wrong argument type
    with pytest.raises(TypeError):
        parse_review_preference(123)  # type: ignore
    
    # Test correct argument type
    result = parse_review_preference("")
    assert isinstance(result, str)
    assert result in ("bot-only", "bot+human")

def test_parse_review_preference_functionality():
    """Test the actual functionality of parse_review_preference."""
    # Test bot-only preference
    description = "Some PR description\n[x] Bot review only"
    result = parse_review_preference(description)
    assert result == "bot-only"
    
    # Test bot+human preference
    description = "Some PR description\n[x] Bot + human review"
    result = parse_review_preference(description)
    assert result == "bot+human"
    
    # Test default case
    description = "Some PR description without any preference"
    result = parse_review_preference(description)
    assert result == "bot+human"  # Default value 