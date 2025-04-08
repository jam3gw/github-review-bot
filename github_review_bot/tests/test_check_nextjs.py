"""
Tests for check_nextjs.py script.
"""

import pytest
from typing import Dict, List
from github_review_bot.scripts.check_nextjs import check_nextjs

def test_check_nextjs_interface():
    """Test the interface of check_nextjs function."""
    # Test missing required argument
    with pytest.raises(TypeError):
        check_nextjs()
    
    # Test wrong argument type
    with pytest.raises(TypeError):
        check_nextjs(123)  # type: ignore
    
    # Test correct argument type
    result = check_nextjs(".")
    assert isinstance(result, list)
    if result:  # If any issues found
        assert isinstance(result[0], dict)
        assert 'type' in result[0]
        assert 'message' in result[0]

def test_check_nextjs_functionality():
    """Test the actual functionality of check_nextjs."""
    # Test with non-Next.js project
    result = check_nextjs(".")
    assert isinstance(result, list)
    
    # TODO: Add test with mock Next.js project structure
    # This would require setting up a test directory with Next.js files 