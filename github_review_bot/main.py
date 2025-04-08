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
import json

def extract_pr_number() -> int:
    """
    Extract the pull request number from environment variables.
    
    Returns:
        int: The pull request number
        
    Raises:
        ValueError: If the PR number cannot be determined
    """
    # Try to get PR number from GitHub Actions environment
    pr_number = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")
    if pr_number:
        return int(pr_number)
    
    # Try to get PR number from GitHub event payload
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and os.path.exists(event_path):
        with open(event_path) as f:
            event_data = json.load(f)
            if "pull_request" in event_data and "number" in event_data["pull_request"]:
                return int(event_data["pull_request"]["number"])
    
    raise ValueError("Could not determine PR number from environment variables")

def main():
    """Main function that runs the review bot."""
    # Get environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")

    # Check if running in GitHub Actions
    is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"

    # Initialize GitHub client
    g = Github(github_token)
    
    # Get repository and PR info from environment
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = extract_pr_number()
    
    if not repo_name or not pr_number:
        raise ValueError("Could not determine repository or PR number")
    
    # Get repository and PR objects
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    print("GitHub Review Bot running...")
    
    # Load config
    config_path = ".github/bot-config.yml"
    print(f"Using config from: {config_path}")
    config = load_config(config_path)
    
    print(f"Running analysis on PR #{pr_number}...")
    
    # Run analysis
    analysis_results = run_analysis(pr, config)
    
    # Generate review content
    review_body, review_action = generate_review(analysis_results, config)
    
    # If running in GitHub Actions and the action would be APPROVE, use COMMENT instead
    if is_github_actions and review_action == "APPROVE":
        review_action = "COMMENT"
        review_body = "✅ " + review_body + "\n\n*Note: This bot cannot directly approve PRs when running in GitHub Actions, but all checks have passed.*"
    
    # Post review
    pr.create_review(
        body=review_body,
        event=review_action
    )
    
    # Post detailed comments if any
    post_comments(pr, analysis_results)
    
    print("Review completed successfully!")
    
    # Exit with status code based on original review action before modification
    sys.exit(0 if review_action == "COMMENT" else 1)

if __name__ == "__main__":
    main() 