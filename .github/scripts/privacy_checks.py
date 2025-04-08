#!/usr/bin/env python3
"""
Script to perform data privacy compliance checks.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Common patterns for PII detection
PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b(\+\d{1,3}[- ]?)?\d{3}[- ]?\d{3}[- ]?\d{4}\b',
    'ssn': r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
    'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
    'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    'password': r'password.*[=:].+',
    'api_key': r'api[_-]?key.*[=:].+',
}

def check_pii(file_content: str, file_path: str) -> List[Dict]:
    """Check for potential PII in code."""
    issues = []
    
    # Skip binary and media files
    if any(file_path.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.pdf', '.zip']):
        return issues
    
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.finditer(pattern, file_content)
        for match in matches:
            # Ignore matches in comments for some PII types
            line_start = file_content.rfind('\n', 0, match.start()) + 1
            line = file_content[line_start:file_content.find('\n', match.start())]
            
            if pii_type in ['email', 'phone'] and (line.strip().startswith('#') or line.strip().startswith('//')):
                continue
            
            issues.append({
                'type': 'pii_scan',
                'severity': 'error',
                'message': f'Potential {pii_type} found in code',
                'line': file_content.count('\n', 0, match.start()) + 1
            })
    
    return issues

def check_gdpr_compliance(file_content: str) -> List[Dict]:
    """Check for GDPR compliance issues."""
    issues = []
    
    # Check for user consent handling
    if re.search(r'user|personal|data', file_content, re.IGNORECASE):
        if not re.search(r'consent|gdpr|privacy', file_content, re.IGNORECASE):
            issues.append({
                'type': 'gdpr_compliance',
                'severity': 'warning',
                'message': 'User data handling found without explicit consent management',
                'line': 1
            })
    
    # Check for data retention policies
    if re.search(r'store|save|database|db', file_content, re.IGNORECASE):
        if not re.search(r'retention|expire|ttl|delete', file_content, re.IGNORECASE):
            issues.append({
                'type': 'gdpr_compliance',
                'severity': 'warning',
                'message': 'Data storage without clear retention policy',
                'line': 1
            })
    
    # Check for data export functionality
    if re.search(r'user.*data|personal.*data', file_content, re.IGNORECASE):
        if not re.search(r'export|download|retrieve', file_content, re.IGNORECASE):
            issues.append({
                'type': 'gdpr_compliance',
                'severity': 'warning',
                'message': 'User data handling without export functionality',
                'line': 1
            })
    
    return issues

def check_ccpa_compliance(file_content: str) -> List[Dict]:
    """Check for CCPA compliance issues."""
    issues = []
    
    # Check for data sale indicators
    if re.search(r'sell|share|transfer|partner', file_content, re.IGNORECASE):
        if not re.search(r'opt.*out|ccpa|privacy', file_content, re.IGNORECASE):
            issues.append({
                'type': 'ccpa_compliance',
                'severity': 'warning',
                'message': 'Potential data sharing without opt-out mechanism',
                'line': 1
            })
    
    # Check for data collection disclosure
    if re.search(r'collect|gather|track', file_content, re.IGNORECASE):
        if not re.search(r'notice|disclosure|privacy.*policy', file_content, re.IGNORECASE):
            issues.append({
                'type': 'ccpa_compliance',
                'severity': 'warning',
                'message': 'Data collection without clear disclosure',
                'line': 1
            })
    
    # Check for deletion requests
    if re.search(r'user.*data|personal.*data', file_content, re.IGNORECASE):
        if not re.search(r'delete|remove|erase', file_content, re.IGNORECASE):
            issues.append({
                'type': 'ccpa_compliance',
                'severity': 'warning',
                'message': 'User data handling without deletion capability',
                'line': 1
            })
    
    return issues

def analyze_file(file_path: str) -> List[Dict]:
    """Analyze a single file for privacy issues."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    issues = []
    issues.extend(check_pii(content, file_path))
    issues.extend(check_gdpr_compliance(content))
    issues.extend(check_ccpa_compliance(content))
    
    return issues

def main():
    """Main function to run privacy checks."""
    # Load bot configuration
    try:
        with open('bot_config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: bot_config.json not found")
        sys.exit(1)
    
    # Only run checks if privacy checks are enabled
    privacy_checks = config.get('data_privacy', {})
    if not any(privacy_checks.values()):
        print("Privacy checks are disabled in configuration")
        sys.exit(0)
    
    # Get changed files
    result = os.popen('git diff --name-only origin/main').read().splitlines()
    
    all_issues = []
    for file_path in result:
        if not os.path.exists(file_path):
            continue
        
        # Skip certain file types
        if any(file_path.endswith(ext) for ext in ['.pyc', '.git', '.env']):
            continue
        
        file_issues = analyze_file(file_path)
        if file_issues:
            all_issues.append({
                'file': file_path,
                'issues': file_issues
            })
    
    # Save results
    with open('privacy_checks_results.json', 'w') as f:
        json.dump(all_issues, f, indent=2)
    
    # Exit with status code
    sys.exit(1 if all_issues else 0)

if __name__ == "__main__":
    main() 