"""
Tests for post_comments.py script.
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, create_autospec
from github import PullRequest
from github_review_bot.scripts.post_comments import post_comments

@pytest.fixture
def mock_pr():
    """Create a mock PR object."""
    pr = create_autospec(PullRequest)
    pr.create_issue_comment = Mock()  # Add mock for the method we use
    return pr

@pytest.fixture
def mock_analysis_results():
    """Create mock analysis results."""
    return {
        'passed': False,
        'issues': [
            {'tool': 'flake8', 'output': 'E501 line too long'},
            {'tool': 'mypy', 'output': 'Type error found'}
        ]
    }

def test_post_comments_interface(mock_pr, mock_analysis_results):
    """Test the interface of post_comments function."""
    # Test wrong argument types
    with pytest.raises(TypeError):
        post_comments("not a PR", mock_analysis_results)
    
    with pytest.raises(TypeError):
        post_comments(mock_pr, "not a dict")
    
    # Test correct argument types
    result = post_comments(mock_pr, mock_analysis_results)
    assert isinstance(result, bool)

def test_post_comments_functionality(mock_pr, mock_analysis_results):
    """Test the actual functionality of post_comments."""
    # Test successful case
    result = post_comments(mock_pr, mock_analysis_results)
    assert result is True
    assert mock_pr.create_issue_comment.call_count == 2  # Two issues should create two comments
    
    # Test with no issues
    mock_pr.create_issue_comment.reset_mock()
    empty_results = {'passed': True, 'issues': []}
    result = post_comments(mock_pr, empty_results)
    assert result is True  # Should succeed but not create new comments
    assert mock_pr.create_issue_comment.call_count == 0  # No comments should be created
    
    # TODO: Add test with mocked GitHub API
    # This would require setting up proper test environment variables
    # and possibly mocking the GitHub API calls 