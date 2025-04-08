#!/usr/bin/env python3
"""
Script to generate a review summary from analysis results.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Tuple

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

def generate_summary_markdown(results: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Generate a markdown summary of the review."""
    if not isinstance(results, dict):
        raise TypeError(f"results must be a dictionary, got {type(results)}")
    if not isinstance(config, dict):
        raise TypeError(f"config must be a dictionary, got {type(config)}")
        
    summary = ["# Code Review Summary\n"]
    
    # Add repository info
    summary.append(f"## Repository Information")
    summary.append(f"- Type: {config.get('repo_type', 'default')}")
    summary.append(f"- Review Strictness: {config.get('review_strictness', 'medium')}\n")
    
    # Add analysis results
    has_issues = False
    
    # Add issues from test case format
    if 'issues' in results:
        has_issues = bool(results['issues'])
        for issue in results['issues']:
            tool = issue.get('tool', '')
            output = issue.get('output', '')
            if tool and output:
                summary.append(f"## {tool.title()} Issues")
                summary.append("```")
                summary.append(str(output))
                summary.append("```")
    
    # Add Python analysis results
    if 'python' in results:
        summary.append("## Python Analysis")
        python_results = results['python']
        if isinstance(python_results, dict):
            for tool, output in python_results.items():
                if output:
                    has_issues = True
                    summary.append(f"### {tool.title()} Issues")
                    summary.append("```")
                    summary.append(str(output))
                    summary.append("```")
    
    # Add JavaScript analysis results
    if 'javascript' in results:
        summary.append("## JavaScript/TypeScript Analysis")
        js_results = results['javascript']
        if isinstance(js_results, dict):
            for tool, output in js_results.items():
                if output:
                    has_issues = True
                    summary.append(f"### {tool.title()} Issues")
                    summary.append("```")
                    summary.append(str(output))
                    summary.append("```")
    
    # Add recommendations
    summary.append("\n## Recommendations")
    if not has_issues:
        summary.append("✅ All automated checks passed successfully!")
    else:
        summary.append("⚠️ Some issues were found during the automated review.")
        summary.append("Please address the issues mentioned above before merging.")
    
    return "\n".join(summary)

def generate_review(analysis_results: Dict[str, Any]) -> Tuple[str, str]:
    """
    Generate a review summary from analysis results.
    
    Args:
        analysis_results: Dictionary containing analysis results with keys:
            - passed: bool indicating if all checks passed
            - issues: list of found issues
            - stats: dict of analysis statistics
            
    Returns:
        Tuple[str, str] containing:
            - review_body: The generated review summary in markdown format
            - review_action: The suggested action ('approve' or 'request_changes')
            
    Raises:
        TypeError: If analysis_results is not a dictionary
    """
    if not isinstance(analysis_results, dict):
        raise TypeError(f"analysis_results must be a dictionary, got {type(analysis_results)}")
    
    # Load configuration
    with open('bot_config.json', 'r') as f:
        config = json.load(f)
    
    # Generate summary markdown
    review_body = generate_summary_markdown(analysis_results, config)
    
    # Determine review action based on analysis results
    review_action = 'approve' if analysis_results.get('passed', False) else 'request_changes'
    
    return review_body, review_action

def main():
    # Generate review
    summary = generate_review()
    
    # Save summary to file
    with open('review_summary.md', 'w') as f:
        f.write(summary)
    
    print("Review summary generated successfully")

if __name__ == "__main__":
    main() 