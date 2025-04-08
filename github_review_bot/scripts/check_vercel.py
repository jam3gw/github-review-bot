#!/usr/bin/env python3
"""
Vercel deployment checks for the GitHub Review Bot.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path

class VercelChecker:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.issues: List[Dict] = []

    def check_vercel_json(self) -> None:
        """Check vercel.json for common issues."""
        config_path = self.repo_path / "vercel.json"
        if not config_path.exists():
            self.issues.append({
                "type": "info",
                "message": "No vercel.json found. Consider adding one for better deployment configuration.",
                "file": "vercel.json"
            })
            return

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            # Check for common issues
            if "rewrites" not in config:
                self.issues.append({
                    "type": "info",
                    "message": "Consider adding rewrites configuration for better routing control.",
                    "file": "vercel.json"
                })

            if "headers" not in config:
                self.issues.append({
                    "type": "info",
                    "message": "Consider adding headers configuration for better security and performance.",
                    "file": "vercel.json"
                })

        except json.JSONDecodeError:
            self.issues.append({
                "type": "error",
                "message": "Invalid vercel.json format.",
                "file": "vercel.json"
            })

    def check_environment_variables(self) -> None:
        """Check for required environment variables."""
        env_files = [
            ".env.local",
            ".env.development",
            ".env.production"
        ]

        for env_file in env_files:
            env_path = self.repo_path / env_file
            if env_path.exists():
                self.issues.append({
                    "type": "warning",
                    "message": f"{env_file} found in repository. Consider using Vercel's environment variables instead.",
                    "file": env_file
                })

    def check_build_settings(self) -> None:
        """Check package.json for Vercel build settings."""
        package_path = self.repo_path / "package.json"
        if not package_path.exists():
            return

        try:
            with open(package_path, 'r') as f:
                package = json.load(f)

            # Check build script
            build_script = package.get("scripts", {}).get("build")
            if not build_script:
                self.issues.append({
                    "type": "error",
                    "message": "No build script found in package.json.",
                    "file": "package.json"
                })
            elif "next build" not in build_script:
                self.issues.append({
                    "type": "warning",
                    "message": "Build script should include 'next build' for Vercel deployment.",
                    "file": "package.json"
                })

            # Check for Vercel CLI
            if "@vercel/cli" not in package.get("devDependencies", {}):
                self.issues.append({
                    "type": "info",
                    "message": "Consider adding @vercel/cli for local development and testing.",
                    "file": "package.json"
                })

        except json.JSONDecodeError:
            self.issues.append({
                "type": "error",
                "message": "Invalid package.json format.",
                "file": "package.json"
            })

    def check_deployment_files(self) -> None:
        """Check for deployment-specific files."""
        # Check for .vercelignore
        if not (self.repo_path / ".vercelignore").exists():
            self.issues.append({
                "type": "info",
                "message": "Consider adding .vercelignore to exclude unnecessary files from deployment.",
                "file": ".vercelignore"
            })

        # Check for Vercel Analytics
        if not (self.repo_path / "package.json").exists():
            return

        try:
            with open(self.repo_path / "package.json", 'r') as f:
                package = json.load(f)
                if "@vercel/analytics" not in package.get("dependencies", {}):
                    self.issues.append({
                        "type": "info",
                        "message": "Consider adding @vercel/analytics for better deployment insights.",
                        "file": "package.json"
                    })
        except:
            pass

    def run_checks(self) -> List[Dict]:
        """Run all Vercel specific checks."""
        self.check_vercel_json()
        self.check_environment_variables()
        self.check_build_settings()
        self.check_deployment_files()
        return self.issues

def check_vercel(repo_path: str) -> List[Dict]:
    """Main function to run Vercel checks."""
    checker = VercelChecker(repo_path)
    return checker.run_checks()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_vercel.py <repo_path>")
        sys.exit(1)
    
    issues = check_vercel(sys.argv[1])
    print(json.dumps(issues, indent=2)) 