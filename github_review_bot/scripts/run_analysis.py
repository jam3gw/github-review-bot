#!/usr/bin/env python3
"""
Script to run code analysis based on repository type and configuration.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def load_config():
    """Load the bot configuration."""
    config_path = 'bot_config.json'
    if not os.path.exists(config_path):
        print("Error: Configuration file not found")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return json.load(f)

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

def main():
    config = load_config()
    all_checks_passed = True
    
    # Run general code analysis
    if config['enabled_checks']['code_style']:
        all_checks_passed &= run_python_analysis()
        all_checks_passed &= run_js_analysis()
    
    # Run specialized analysis based on repo type
    if config['repo_type'] == 'ai_agent':
        all_checks_passed &= run_ai_analysis()
    elif config['repo_type'] == 'api':
        all_checks_passed &= run_api_analysis()
    
    # Set GitHub Actions output
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"all_checks_passed={str(all_checks_passed).lower()}\n")
    
    print(f"All checks passed: {all_checks_passed}")
    sys.exit(0 if all_checks_passed else 1)

if __name__ == "__main__":
    main() 