#!/usr/bin/env python3
"""
Script to post review comments to a pull request.
"""

import os
import sys
from typing import Optional, Dict, Any
from github import Github, PullRequest

def post_comments(pr: PullRequest, analysis_results: Dict[str, Any]) -> bool:
    """
    Post review comments to a pull request.
    
    Args:
        pr: The GitHub pull request object to post comments to
        analysis_results: Dictionary containing analysis results
        
    Returns:
        bool: True if comments were posted successfully, False otherwise
        
    Raises:
        TypeError: If arguments are of wrong type
    """
    # Check if pr has the required method
    if not hasattr(pr, 'create_issue_comment') or not callable(getattr(pr, 'create_issue_comment')):
        raise TypeError("pr must be a PullRequest object with create_issue_comment method")
    if not isinstance(analysis_results, dict):
        raise TypeError(f"analysis_results must be a dictionary, got {type(analysis_results)}")
    
    try:
        # Extract issues from analysis results
        issues = analysis_results.get('issues', [])
        
        # Post each issue as a separate comment
        for issue in issues:
            comment = f"**{issue.get('tool', 'Analysis')} Issue:**\n\n```\n{issue.get('output', '')}\n```"
            pr.create_issue_comment(comment)
        
        print(f"Posted {len(issues)} review comments successfully")
        return True
    except Exception as e:
        print(f"Error posting review comments: {e}")
        return False

def main():
    """This script is not meant to be run directly."""
    print("Error: This script should be imported, not run directly")
    sys.exit(1)

if __name__ == "__main__":
    main() 