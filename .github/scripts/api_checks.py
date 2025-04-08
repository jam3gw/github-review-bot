#!/usr/bin/env python3
"""
Script to perform API-specific checks on repositories.
"""

import os
import sys
import json
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional

def validate_openapi_spec(spec_path: str) -> List[Dict]:
    """Validate OpenAPI/Swagger specification."""
    issues = []
    
    try:
        with open(spec_path, 'r') as f:
            spec = yaml.safe_load(f)
        
        # Check for required OpenAPI fields
        required_fields = ['openapi', 'info', 'paths']
        for field in required_fields:
            if field not in spec:
                issues.append({
                    'type': 'openapi_validation',
                    'severity': 'error',
                    'message': f'Missing required field: {field}',
                    'line': 1
                })
        
        # Check paths for common issues
        if 'paths' in spec:
            for path, methods in spec['paths'].items():
                for method, details in methods.items():
                    # Check for response definitions
                    if 'responses' not in details:
                        issues.append({
                            'type': 'openapi_validation',
                            'severity': 'error',
                            'message': f'Missing responses for {method.upper()} {path}',
                            'line': 1
                        })
                    
                    # Check for parameters documentation
                    if 'parameters' in details:
                        for param in details['parameters']:
                            if 'description' not in param:
                                issues.append({
                                    'type': 'openapi_validation',
                                    'severity': 'warning',
                                    'message': f'Missing parameter description in {method.upper()} {path}',
                                    'line': 1
                                })
    
    except Exception as e:
        issues.append({
            'type': 'openapi_validation',
            'severity': 'error',
            'message': f'Failed to parse OpenAPI specification: {str(e)}',
            'line': 1
        })
    
    return issues

def check_error_handling(file_content: str) -> List[Dict]:
    """Check API error handling practices."""
    issues = []
    
    # Check for try-except blocks in route handlers
    route_patterns = [
        r'@app\.route',
        r'@router\.get',
        r'@router\.post',
        r'@router\.put',
        r'@router\.delete'
    ]
    
    for pattern in route_patterns:
        matches = re.finditer(pattern, file_content)
        for match in matches:
            # Look for try-except in the route handler
            handler_start = match.end()
            next_def = file_content.find('def', handler_start)
            if next_def == -1:
                continue
            
            handler_end = file_content.find('def', next_def + 1)
            if handler_end == -1:
                handler_end = len(file_content)
            
            handler_code = file_content[next_def:handler_end]
            if 'try:' not in handler_code:
                issues.append({
                    'type': 'error_handling',
                    'severity': 'warning',
                    'message': 'Add error handling to route handler',
                    'line': file_content.count('\n', 0, next_def) + 1
                })
    
    return issues

def check_rate_limiting(file_content: str) -> List[Dict]:
    """Check rate limiting implementation."""
    issues = []
    
    # Look for common rate limiting decorators/middleware
    rate_limit_patterns = [
        r'@limiter\.limit',
        r'RateLimitMiddleware',
        r'ThrottlingMiddleware',
        r'rate_limit',
        r'throttle_classes'
    ]
    
    has_rate_limiting = any(re.search(pattern, file_content) for pattern in rate_limit_patterns)
    
    if not has_rate_limiting and any(pattern in file_content for pattern in ['@app.route', '@router']):
        issues.append({
            'type': 'rate_limiting',
            'severity': 'warning',
            'message': 'Consider implementing rate limiting for API endpoints',
            'line': 1
        })
    
    return issues

def check_authentication(file_content: str) -> List[Dict]:
    """Check authentication implementation."""
    issues = []
    
    # Look for routes without authentication
    route_patterns = [
        (r'@app\.route.*?\ndef\s+(\w+)', 'flask'),
        (r'@router\.(get|post|put|delete).*?\ndef\s+(\w+)', 'fastapi')
    ]
    
    auth_patterns = [
        r'@auth\.',
        r'@login_required',
        r'@jwt_required',
        r'authenticate',
        r'Authorization',
        r'Bearer',
        r'verify_token'
    ]
    
    for route_pattern, framework in route_patterns:
        matches = re.finditer(route_pattern, file_content, re.DOTALL)
        for match in matches:
            # Get the route handler code
            start = match.start()
            end = file_content.find('def', start + 1)
            if end == -1:
                end = len(file_content)
            handler_code = file_content[start:end]
            
            # Check if any auth pattern is present
            if not any(re.search(auth_pattern, handler_code) for auth_pattern in auth_patterns):
                issues.append({
                    'type': 'authentication',
                    'severity': 'warning',
                    'message': f'Route handler might be missing authentication',
                    'line': file_content.count('\n', 0, start) + 1
                })
    
    return issues

def main():
    """Main function to run API checks."""
    # Load bot configuration
    try:
        with open('bot_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: bot_config.json not found")
        sys.exit(1)
    
    # Only run checks if API checks are enabled
    api_checks = config.get('api_checks', {})
    if not any(api_checks.values()):
        print("API checks are disabled in configuration")
        sys.exit(0)
    
    # Get changed files
    result = os.popen('git diff --name-only origin/main').read().splitlines()
    
    all_issues = []
    
    # Check OpenAPI specification
    if api_checks.get('openapi_validation'):
        for spec_file in ['openapi.yaml', 'openapi.yml', 'swagger.yaml', 'swagger.yml']:
            if spec_file in result and os.path.exists(spec_file):
                issues = validate_openapi_spec(spec_file)
                if issues:
                    all_issues.append({
                        'file': spec_file,
                        'issues': issues
                    })
    
    # Check Python API files
    py_files = [f for f in result if f.endswith('.py')]
    for file_path in py_files:
        if not os.path.exists(file_path):
            continue
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        file_issues = []
        
        if api_checks.get('error_handling'):
            file_issues.extend(check_error_handling(content))
        
        if api_checks.get('rate_limiting'):
            file_issues.extend(check_rate_limiting(content))
        
        if api_checks.get('authentication'):
            file_issues.extend(check_authentication(content))
        
        if file_issues:
            all_issues.append({
                'file': file_path,
                'issues': file_issues
            })
    
    # Save results
    with open('api_checks_results.json', 'w') as f:
        json.dump(all_issues, f, indent=2)
    
    # Exit with status code
    sys.exit(1 if all_issues else 0)

if __name__ == "__main__":
    main() 