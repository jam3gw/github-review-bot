#!/usr/bin/env python3
"""
Script to post review comments to a pull request.
"""

import os
import sys
from typing import Optional
from github import Github

def post_comments(summary: str) -> bool:
    """
    Post review comments to a pull request.
    
    Args:
        summary: The review summary text to post
        
    Returns:
        bool: True if comments were posted successfully, False otherwise
    """
    # Get environment variables
    token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    pr_number = os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER')
    
    if not all([token, repo_name, pr_number]):
        print("Error: Missing required environment variables")
        return False
    
    try:
        # Initialize GitHub client
        g = Github(token)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))
        
        # Post review comment
        pr.create_issue_comment(summary)
        print("Review comment posted successfully")
        return True
    except Exception as e:
        print(f"Error posting review comment: {e}")
        return False

def main():
    # Read review summary
    try:
        with open('review_summary.md', 'r') as f:
            summary = f.read()
    except FileNotFoundError:
        print("Error: Review summary file not found")
        sys.exit(1)
    
    # Post comments
    success = post_comments(summary)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 