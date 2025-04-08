"""
Pytest configuration and fixtures for automated interface testing.
"""

import inspect
from typing import get_type_hints, Any, Dict, List, Optional, Union, Tuple, Literal
import pytest
from github import PullRequest
from github_review_bot.scripts import (
    load_config,
    generate_review,
    run_analysis,
    post_comments,
    check_nextjs,
    check_vercel,
    parse_review_preference
)

def verify_interface(func: Any, expected_params: Dict[str, type], expected_return: type) -> None:
    """
    Verify a function's interface matches expectations.
    
    Args:
        func: The function to verify
        expected_params: Dictionary of parameter names to their expected types
        expected_return: Expected return type annotation
    
    Raises:
        AssertionError: If the interface doesn't match expectations
    """
    sig = inspect.signature(func)
    hints = get_type_hints(func)
    
    # Verify parameters
    for name, expected_type in expected_params.items():
        assert name in sig.parameters, f"Missing parameter: {name}"
        if name in hints:
            assert hints[name] == expected_type, f"Wrong type for {name}: expected {expected_type}, got {hints[name]}"
    
    # Verify return type
    if expected_return is not None:
        assert 'return' in hints, "Missing return type annotation"
        assert hints['return'] == expected_return, f"Wrong return type: expected {expected_return}, got {hints['return']}"

@pytest.fixture(autouse=True)
def verify_interfaces():
    """Automatically verify all script interfaces match their contracts."""
    # Verify load_config interface
    verify_interface(
        load_config.load_config,
        {'config_path': str},
        Dict[str, Any]
    )
    
    # Verify generate_review interface
    verify_interface(
        generate_review.generate_review,
        {
            'analysis_results': Dict[str, Any],
            'config': Dict[str, Any]
        },
        Tuple[str, str]
    )
    
    # Verify run_analysis interface
    verify_interface(
        run_analysis.run_analysis,
        {'pr': Any, 'config': Dict[str, Any]},
        Dict[str, Any]
    )
    
    # Verify post_comments interface
    verify_interface(
        post_comments.post_comments,
        {
            'pr': PullRequest,
            'analysis_results': Dict[str, Any]
        },
        bool
    )
    
    # Verify check_nextjs interface
    verify_interface(
        check_nextjs.check_nextjs,
        {'repo_path': str},
        List[Dict[str, Any]]
    )
    
    # Verify check_vercel interface
    verify_interface(
        check_vercel.check_vercel,
        {'repo_path': str},
        List[Dict[str, Any]]
    )
    
    # Verify parse_review_preference interface
    verify_interface(
        parse_review_preference.parse_review_preference,
        {'description': str},
        Literal["bot-only", "bot+human"]
    ) 