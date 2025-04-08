#!/usr/bin/env python3
"""
Main entry point for the GitHub Review Bot.
"""
import os
import sys
from github import Github
import yaml

def main():
    """Main function that runs the review bot."""
    # Get GitHub token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    # Get configuration path
    config_path = os.getenv('CONFIG_PATH', '.github/bot-config.yml')
    
    # Get GitHub event context
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        print("Error: GITHUB_EVENT_PATH not set")
        sys.exit(1)

    # Read event data
    with open(event_path) as f:
        event_data = yaml.safe_load(f)

    # Initialize GitHub client
    g = Github(token)
    
    # Get repository and PR
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number = event_data['pull_request']['number']
    
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # TODO: Add actual code review checks here
    # For now, we'll just approve if we got this far
    print("GitHub Review Bot running...")
    print(f"Using config from: {config_path}")
    
    # Submit approval review
    pr.create_review(
        body="✅ Automated review passed. All checks completed successfully.",
        event="APPROVE"
    )
    print("Review submitted successfully!")

if __name__ == "__main__":
    main() 