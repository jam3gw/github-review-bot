#!/usr/bin/env python3
"""
Script to load and parse the repository configuration from .github/bot-config.yml
"""

import os
import sys
import yaml
import json

CONFIG_PATH = ".github/bot-config.yml"

# Default configuration
DEFAULT_CONFIG = {
    "repo_type": "default",
    "review_strictness": "medium",
    "enabled_checks": {
        "code_style": True,
        "security": True,
        "performance": True,
        "test_coverage": True,
        "documentation": True
    },
    "ai_checks": {
        "prompt_engineering": False,
        "model_versioning": False,
        "response_validation": False
    },
    "api_checks": {
        "openapi_validation": False,
        "error_handling": False,
        "rate_limiting": False,
        "authentication": False
    },
    "data_privacy": {
        "pii_scan": True,
        "gdpr_compliance": True,
        "ccpa_compliance": True
    }
}

def load_config(config_path=CONFIG_PATH):
    """Load repository configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file. Defaults to CONFIG_PATH.
    """
    config = DEFAULT_CONFIG.copy()
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                
            # Update config with user settings
            if user_config:
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                        # Merge dictionaries for nested configs
                        config[key].update(value)
                    else:
                        # Replace top-level values
                        config[key] = value
        else:
            print(f"Configuration file not found at {config_path}, using defaults.")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Using default configuration.")
    
    return config

def set_github_actions_output(config):
    """Set GitHub Actions outputs from the configuration."""
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"repo_type={config['repo_type']}\n")
        f.write(f"review_strictness={config['review_strictness']}\n")
        
        # Convert dictionaries to JSON strings
        for key in ['enabled_checks', 'ai_checks', 'api_checks', 'data_privacy']:
            if key in config:
                json_value = json.dumps(config[key]).replace('"', '\\"')
                f.write(f"{key}={json_value}\n")

def main():
    config = load_config()
    
    # Save config for other scripts to use
    with open('bot_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Set outputs for GitHub Actions
    set_github_actions_output(config)
    
    print(f"Loaded configuration for repository type: {config['repo_type']}")
    print(f"Review strictness: {config['review_strictness']}")

if __name__ == "__main__":
    main() 