#!/usr/bin/env python3
"""
Script to generate a review summary from analysis results.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

def load_analysis_results():
    """Load all analysis results from JSON files."""
    results = {}
    
    # Load Python analysis results
    if os.path.exists('analysis_results.json'):
        with open('analysis_results.json', 'r') as f:
            results['python'] = json.load(f)
    
    # Load JavaScript analysis results
    if os.path.exists('js_analysis_results.json'):
        with open('js_analysis_results.json', 'r') as f:
            results['javascript'] = json.load(f)
    
    return results

def generate_summary_markdown(results, config):
    """Generate a markdown summary of the review."""
    summary = ["# Code Review Summary\n"]
    
    # Add repository info
    summary.append(f"## Repository Information")
    summary.append(f"- Type: {config['repo_type']}")
    summary.append(f"- Review Strictness: {config['review_strictness']}\n")
    
    # Add Python analysis results
    if 'python' in results:
        summary.append("## Python Analysis")
        if results['python']['flake8']:
            summary.append("### Flake8 Issues")
            summary.append("```")
            summary.append(results['python']['flake8'])
            summary.append("```")
        
        if results['python']['black']:
            summary.append("### Black Formatting Issues")
            summary.append("```")
            summary.append(results['python']['black'])
            summary.append("```")
        
        if results['python']['bandit']:
            summary.append("### Security Issues (Bandit)")
            summary.append("```")
            summary.append(results['python']['bandit'])
            summary.append("```")
    
    # Add JavaScript analysis results
    if 'javascript' in results:
        summary.append("## JavaScript/TypeScript Analysis")
        if results['javascript']['eslint']:
            summary.append("### ESLint Issues")
            summary.append("```")
            summary.append(results['javascript']['eslint'])
            summary.append("```")
        
        if results['javascript']['typescript']:
            summary.append("### TypeScript Type Checking Issues")
            summary.append("```")
            summary.append(results['javascript']['typescript'])
            summary.append("```")
    
    # Add recommendations
    summary.append("\n## Recommendations")
    if not any(results.values()):
        summary.append("✅ All automated checks passed successfully!")
    else:
        summary.append("⚠️ Some issues were found during the automated review.")
        summary.append("Please address the issues mentioned above before merging.")
    
    return "\n".join(summary)

def generate_review() -> str:
    """
    Generate a review summary from analysis results.
    
    Returns:
        str: The generated review summary in markdown format.
    """
    # Load configuration
    with open('bot_config.json', 'r') as f:
        config = json.load(f)
    
    # Load analysis results
    results = load_analysis_results()
    
    # Generate and return summary
    return generate_summary_markdown(results, config)

def main():
    # Generate review
    summary = generate_review()
    
    # Save summary to file
    with open('review_summary.md', 'w') as f:
        f.write(summary)
    
    print("Review summary generated successfully")

if __name__ == "__main__":
    main() 