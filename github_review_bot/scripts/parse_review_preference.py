#!/usr/bin/env python3
"""
Script to parse the review preference from a pull request.
"""

import os
import sys
import re
from github import Github

def parse_pr_description(description):
    """Parse PR description to determine review type."""
    # Check for bot-only review checkbox
    bot_only_pattern = r'\[x\]\s*Bot\s*review\s*only'
    if re.search(bot_only_pattern, description, re.IGNORECASE):
        return "bot-only"
    
    # Check for bot+human review checkbox
    bot_human_pattern = r'\[x\]\s*Bot\s*\+\s*human\s*review'
    if re.search(bot_human_pattern, description, re.IGNORECASE):
        return "bot+human"
    
    # Default to bot+human review if no preference specified
    return "bot+human"

def main():
    # Get PR number from environment
    pr_number = os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER')
    if not pr_number:
        print("Error: PR number not found in environment")
        sys.exit(1)
    
    # Initialize GitHub client
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GitHub token not found in environment")
        sys.exit(1)
    
    g = Github(token)
    
    # Get repository information
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    if not repo_name:
        print("Error: Repository name not found in environment")
        sys.exit(1)
    
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    
    # Parse review preference
    review_type = parse_pr_description(pr.body)
    
    # Set GitHub Actions output
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"review_type={review_type}\n")
    
    print(f"Review type determined: {review_type}")

if __name__ == "__main__":
    main() 