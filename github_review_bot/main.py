#!/usr/bin/env python3
"""
Main entry point for the GitHub Review Bot.
"""
import os
import sys
from github import Github
import yaml
from .scripts.load_config import load_config
from .scripts.run_analysis import run_analysis
from .scripts.generate_review import generate_review
from .scripts.post_comments import post_comments

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
    
    print("GitHub Review Bot running...")
    print(f"Using config from: {config_path}")

    # Load configuration
    config = load_config(config_path)
    
    # Run analysis
    analysis_results = run_analysis(pr, config)
    
    # Generate review content
    review_body, review_action = generate_review(analysis_results)
    
    # Post review
    pr.create_review(
        body=review_body,
        event=review_action  # Will be "APPROVE" or "REQUEST_CHANGES"
    )
    
    # Post detailed comments if any
    post_comments(pr, analysis_results)
    
    print("Review completed successfully!")
    
    # Exit with status code based on review action
    sys.exit(0 if review_action == "APPROVE" else 1)

if __name__ == "__main__":
    main() 