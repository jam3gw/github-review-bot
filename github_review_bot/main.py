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
    
    # Initialize GitHub client
    g = Github(token)
    
    # TODO: Implement actual review logic here
    print("GitHub Review Bot running...")
    print(f"Using config from: {config_path}")

if __name__ == "__main__":
    main() 