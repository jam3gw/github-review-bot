"""
Tests for run_analysis.py script.
"""

import pytest
from typing import Dict, Any, List, Union
from unittest.mock import Mock, create_autospec
from github import PullRequest, PaginatedList, File
from github_review_bot.scripts.run_analysis import run_analysis

class MockPullRequest:
    """A simple class that mimics the PullRequest interface."""
    def __init__(self, number: int, files: List[Any]):
        self.number = number
        self._files = files
    
    def get_files(self):
        return self._files

@pytest.fixture
def mock_pr():
    """Create a mock PR object."""
    # Create a mock file
    mock_file = Mock(spec=File)
    mock_file.filename = "test.py"
    mock_file.status = "modified"
    mock_file.additions = 10
    mock_file.deletions = 5
    mock_file.changes = 15
    
    # Create a list of files
    mock_files = [mock_file]
    
    # Create the PR mock
    pr = MockPullRequest(123, mock_files)
    
    return pr

def test_run_analysis_interface(mock_pr):
    """Test the interface of run_analysis function."""
    # Test missing required arguments
    with pytest.raises(TypeError):
        run_analysis()
    
    with pytest.raises(TypeError):
        run_analysis(pr=None)  # type: ignore
    
    # Test wrong argument types
    with pytest.raises(TypeError):
        run_analysis("not a PR", {})  # type: ignore
    
    with pytest.raises(TypeError):
        run_analysis(mock_pr, "not a dict")  # type: ignore
    
    # Test return type
    result = run_analysis(mock_pr, {})
    assert isinstance(result, dict)
    assert 'passed' in result
    assert 'issues' in result
    assert 'stats' in result

def test_run_analysis_functionality(mock_pr):
    """Test the actual functionality of run_analysis."""
    # Test with empty config
    result = run_analysis(mock_pr, {})
    assert result['passed'] is True  # No checks enabled = pass
    assert len(result['issues']) == 0
    assert isinstance(result['stats'], dict)
    
    # Test with some checks enabled
    config = {
        'rules': {
            'code_style': True
        }
    }
    result = run_analysis(mock_pr, config)
    assert isinstance(result['passed'], bool)
    assert isinstance(result['issues'], list)
    assert isinstance(result['stats'], dict) 