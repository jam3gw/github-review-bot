#!/usr/bin/env python3
"""
Script to perform AI-specific checks on repositories.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

def check_prompt_engineering(file_content: str) -> List[Dict]:
    """Check prompt engineering best practices."""
    issues = []
    
    # Check for hardcoded prompts without variables
    hardcoded_prompt_pattern = r'""".*?(system:|assistant:|user:).*?"""'
    matches = re.finditer(hardcoded_prompt_pattern, file_content, re.MULTILINE | re.DOTALL)
    for match in matches:
        if not re.search(r'\{.*?\}', match.group(0)):  # No variables in prompt
            issues.append({
                'type': 'prompt_engineering',
                'severity': 'warning',
                'message': 'Consider parameterizing hardcoded prompts for better reusability',
                'line': file_content.count('\n', 0, match.start()) + 1
            })
    
    # Check for missing system prompts
    if re.search(r'(assistant:|user:)', file_content, re.IGNORECASE) and not re.search(r'system:', file_content, re.IGNORECASE):
        issues.append({
            'type': 'prompt_engineering',
            'severity': 'warning',
            'message': 'Consider adding a system prompt to better control AI behavior',
            'line': 1
        })
    
    return issues

def check_model_versioning(file_content: str) -> List[Dict]:
    """Check model versioning practices."""
    issues = []
    
    # Check for hardcoded model versions
    model_patterns = [
        r'gpt-3\.5-turbo(?!-\d{4})',  # Missing specific version
        r'gpt-4(?!-\d{4})',  # Missing specific version
        r'text-davinci-003',  # Deprecated model
    ]
    
    for pattern in model_patterns:
        matches = re.finditer(pattern, file_content)
        for match in matches:
            issues.append({
                'type': 'model_versioning',
                'severity': 'error',
                'message': 'Use specific model versions (e.g., gpt-4-0125-preview) for reproducibility',
                'line': file_content.count('\n', 0, match.start()) + 1
            })
    
    return issues

def check_response_validation(file_content: str) -> List[Dict]:
    """Check response validation practices."""
    issues = []
    
    # Check for direct response usage without validation
    validation_patterns = [
        (r'\.choices\[0\]\.message\.content', r'(try|except|validate|schema)'),
        (r'\.generations\[0\]\.text', r'(try|except|validate|schema)'),
    ]
    
    for use_pattern, validation_pattern in validation_patterns:
        matches = re.finditer(use_pattern, file_content)
        for match in matches:
            # Look for validation code around the usage
            context_start = max(0, match.start() - 200)
            context_end = min(len(file_content), match.end() + 200)
            context = file_content[context_start:context_end]
            
            if not re.search(validation_pattern, context):
                issues.append({
                    'type': 'response_validation',
                    'severity': 'warning',
                    'message': 'Add response validation to handle potential AI hallucinations or errors',
                    'line': file_content.count('\n', 0, match.start()) + 1
                })
    
    return issues

def analyze_file(file_path: str) -> List[Dict]:
    """Analyze a single file for AI-related issues."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    issues = []
    issues.extend(check_prompt_engineering(content))
    issues.extend(check_model_versioning(content))
    issues.extend(check_response_validation(content))
    
    return issues

def main():
    """Main function to run AI checks."""
    # Load bot configuration
    try:
        with open('bot_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: bot_config.json not found")
        sys.exit(1)
    
    # Only run checks if AI checks are enabled
    if not config.get('ai_checks', {}).get('prompt_engineering', False) and \
       not config.get('ai_checks', {}).get('model_versioning', False) and \
       not config.get('ai_checks', {}).get('response_validation', False):
        print("AI checks are disabled in configuration")
        sys.exit(0)
    
    # Get changed files
    result = os.popen('git diff --name-only origin/main').read().splitlines()
    py_files = [f for f in result if f.endswith('.py')]
    
    all_issues = []
    for file_path in py_files:
        if os.path.exists(file_path):
            file_issues = analyze_file(file_path)
            if file_issues:
                all_issues.append({
                    'file': file_path,
                    'issues': file_issues
                })
    
    # Save results
    with open('ai_checks_results.json', 'w') as f:
        json.dump(all_issues, f, indent=2)
    
    # Exit with status code
    sys.exit(1 if all_issues else 0)

if __name__ == "__main__":
    main() 