#!/usr/bin/env python3
"""
Script to run code analysis based on repository type and configuration.
"""

import os
import sys
import json
import subprocess
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple
from github import PullRequest
from unittest.mock import Mock

# Import our new checkers
from .check_nextjs import check_nextjs
from .check_vercel import check_vercel
from .load_config import load_config

def run_python_analysis():
    """Run Python code analysis tools."""
    print("Running Python code analysis...")
    
    # Get changed Python files
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'origin/main'],
        capture_output=True,
        text=True
    )
    py_files = [f for f in result.stdout.splitlines() if f.endswith('.py')]
    
    if not py_files:
        print("No Python files changed in this PR")
        return True
    
    # Run flake8
    flake8_result = subprocess.run(
        ['flake8'] + py_files,
        capture_output=True,
        text=True
    )
    
    # Run black
    black_result = subprocess.run(
        ['black', '--check'] + py_files,
        capture_output=True,
        text=True
    )
    
    # Run bandit for security
    bandit_result = subprocess.run(
        ['bandit', '-r'] + py_files,
        capture_output=True,
        text=True
    )
    
    # Save results
    with open('analysis_results.json', 'w') as f:
        json.dump({
            'flake8': flake8_result.stdout,
            'black': black_result.stdout,
            'bandit': bandit_result.stdout
        }, f)
    
    return all(r.returncode == 0 for r in [flake8_result, black_result, bandit_result])

def run_js_analysis():
    """Run JavaScript/TypeScript code analysis."""
    print("Running JavaScript/TypeScript analysis...")
    
    # Get changed JS/TS files
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'origin/main'],
        capture_output=True,
        text=True
    )
    js_files = [f for f in result.stdout.splitlines() 
                if f.endswith(('.js', '.jsx', '.ts', '.tsx'))]
    
    if not js_files:
        print("No JavaScript/TypeScript files changed in this PR")
        return True
    
    # Check if package.json exists
    if not os.path.exists('package.json'):
        print("No package.json found, skipping JavaScript analysis")
        return True
    
    # Install dependencies if needed
    subprocess.run(['npm', 'install'], capture_output=True)
    
    # Run ESLint
    eslint_result = subprocess.run(
        ['npx', 'eslint'] + js_files,
        capture_output=True,
        text=True
    )
    
    # Run TypeScript type checking if tsconfig.json exists
    ts_result = True
    if os.path.exists('tsconfig.json'):
        ts_result = subprocess.run(
            ['npx', 'tsc', '--noEmit'],
            capture_output=True,
            text=True
        )
    
    # Save results
    with open('js_analysis_results.json', 'w') as f:
        json.dump({
            'eslint': eslint_result.stdout,
            'typescript': ts_result.stdout if isinstance(ts_result, subprocess.CompletedProcess) else ''
        }, f)
    
    return all(r.returncode == 0 for r in [eslint_result, ts_result] 
              if isinstance(r, subprocess.CompletedProcess))

def run_nextjs_analysis() -> bool:
    """Run Next.js specific analysis."""
    print("Running Next.js analysis...")
    repo_path = os.getcwd()
    issues = check_nextjs(repo_path)
    
    # Save results
    with open('nextjs_analysis_results.json', 'w') as f:
        json.dump(issues, f, indent=2)
    
    # Consider the check failed if there are any error-level issues
    return not any(issue['type'] == 'error' for issue in issues)

def run_vercel_analysis() -> bool:
    """Run Vercel deployment analysis."""
    print("Running Vercel deployment analysis...")
    repo_path = os.getcwd()
    issues = check_vercel(repo_path)
    
    # Save results
    with open('vercel_analysis_results.json', 'w') as f:
        json.dump(issues, f, indent=2)
    
    # Consider the check failed if there are any error-level issues
    return not any(issue['type'] == 'error' for issue in issues)

def run_frontend_analysis() -> bool:
    """Run frontend-specific analysis."""
    print("Running frontend analysis...")
    all_checks_passed = True
    
    # Run Next.js checks if it's a Next.js project
    if os.path.exists('next.config.js'):
        all_checks_passed &= run_nextjs_analysis()
    
    # Run Vercel checks if it's a Vercel project
    if os.path.exists('vercel.json') or os.path.exists('.vercel'):
        all_checks_passed &= run_vercel_analysis()
    
    # Run general JS/TS analysis
    all_checks_passed &= run_js_analysis()
    
    return all_checks_passed

def run_ai_analysis():
    """Run AI-specific analysis."""
    print("Running AI-specific analysis...")
    # TODO: Implement AI-specific checks
    return True

def run_api_analysis():
    """Run API-specific analysis."""
    print("Running API-specific analysis...")
    # TODO: Implement API-specific checks
    return True

def run_analysis(pr, config) -> Dict[str, Any]:
    """
    Main analysis function that runs all configured checks on a PR.
    
    Args:
        pr: The GitHub pull request object
        config: The bot configuration dictionary
    
    Returns:
        Dict containing analysis results with keys:
        - passed: bool indicating if all checks passed
        - issues: list of found issues
        - stats: dict of analysis statistics
        
    Raises:
        TypeError: If pr is not a PullRequest object or config is not a dictionary
    """
    # Type checking
    if not hasattr(pr, 'number') or not hasattr(pr, 'get_files'):
        raise TypeError(f"pr must be a PullRequest object with number and get_files attributes, got {type(pr)}")
    if not isinstance(config, dict):
        raise TypeError(f"config must be a dictionary, got {type(config)}")
    
    print(f"Running analysis on PR #{pr.number}...")
    results = {
        'passed': True,
        'issues': [],
        'stats': {}
    }
    
    # Run general code analysis based on file types
    if config.get('rules', {}).get('code_style', True):
        if any(f.endswith('.py') for f in os.listdir('.')):
            py_passed = run_python_analysis()
            results['passed'] &= py_passed
            
        if any(f.endswith(('.js', '.jsx', '.ts', '.tsx')) for f in os.listdir('.')):
            js_passed = run_js_analysis()
            results['passed'] &= js_passed
    
    # Run specialized analysis based on repo type
    repo_type = config.get('type', 'default')
    if repo_type == 'frontend':
        frontend_passed = run_frontend_analysis()
        results['passed'] &= frontend_passed
    elif repo_type == 'ai_agent':
        ai_passed = run_ai_analysis()
        results['passed'] &= ai_passed
    elif repo_type == 'api':
        api_passed = run_api_analysis()
        results['passed'] &= api_passed
    
    # Load and combine all results
    for result_file in ['analysis_results.json', 'js_analysis_results.json', 
                       'nextjs_analysis_results.json', 'vercel_analysis_results.json']:
        if os.path.exists(result_file):
            with open(result_file) as f:
                file_results = json.load(f)
                results['issues'].extend(file_results if isinstance(file_results, list) 
                                      else [{'tool': k, 'output': v} for k, v in file_results.items()])
    
    return results

def main():
    config = load_config()
    all_checks_passed = True
    
    # Run general code analysis based on file types
    if config.get('rules', {}).get('code_style', True):
        if any(f.endswith('.py') for f in os.listdir('.')):
            all_checks_passed &= run_python_analysis()
        if any(f.endswith(('.js', '.jsx', '.ts', '.tsx')) for f in os.listdir('.')):
            all_checks_passed &= run_js_analysis()
    
    # Run specialized analysis based on repo type
    repo_type = config.get('type', 'default')
    if repo_type == 'frontend':
        all_checks_passed &= run_frontend_analysis()
    elif repo_type == 'ai_agent':
        all_checks_passed &= run_ai_analysis()
    elif repo_type == 'api':
        all_checks_passed &= run_api_analysis()
    
    # Set GitHub Actions output
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"all_checks_passed={str(all_checks_passed).lower()}\n")
    
    print(f"All checks passed: {all_checks_passed}")
    sys.exit(0 if all_checks_passed else 1)

if __name__ == "__main__":
    main() 