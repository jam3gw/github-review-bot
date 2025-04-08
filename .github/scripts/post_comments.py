#!/usr/bin/env python3
"""
Script to post review comments to a pull request.
"""

import os
import sys
from github import Github

def main():
    # Get environment variables
    token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    pr_number = os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER')
    
    if not all([token, repo_name, pr_number]):
        print("Error: Missing required environment variables")
        sys.exit(1)
    
    # Initialize GitHub client
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    
    # Read review summary
    try:
        with open('review_summary.md', 'r') as f:
            summary = f.read()
    except FileNotFoundError:
        print("Error: Review summary file not found")
        sys.exit(1)
    
    # Post review comment
    try:
        pr.create_issue_comment(summary)
        print("Review comment posted successfully")
    except Exception as e:
        print(f"Error posting review comment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 