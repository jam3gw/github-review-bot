#!/usr/bin/env python3
"""
Next.js specific checks for the GitHub Review Bot.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path

class NextJSChecker:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.issues: List[Dict] = []

    def check_next_config(self) -> None:
        """Check next.config.js for common issues."""
        config_path = self.repo_path / "next.config.js"
        if not config_path.exists():
            self.issues.append({
                "type": "warning",
                "message": "No next.config.js found. Consider adding one for better configuration control.",
                "file": "next.config.js"
            })
            return

        try:
            with open(config_path, 'r') as f:
                content = f.read()
                
            # Check for common issues
            if "images.unoptimized" in content:
                self.issues.append({
                    "type": "warning",
                    "message": "Images are set to unoptimized. Consider enabling image optimization.",
                    "file": "next.config.js"
                })
                
            if "swcMinify" not in content:
                self.issues.append({
                    "type": "info",
                    "message": "Consider enabling swcMinify for faster builds.",
                    "file": "next.config.js"
                })

        except Exception as e:
            self.issues.append({
                "type": "error",
                "message": f"Error reading next.config.js: {str(e)}",
                "file": "next.config.js"
            })

    def check_app_directory(self) -> None:
        """Check for app directory structure and conventions."""
        app_dir = self.repo_path / "app"
        if not app_dir.exists():
            self.issues.append({
                "type": "warning",
                "message": "No app directory found. Consider using the App Router for better performance and features.",
                "file": "app"
            })
            return

        # Check for common app directory issues
        if (app_dir / "layout.tsx").exists():
            # Check for metadata
            layout_content = (app_dir / "layout.tsx").read_text()
            if "metadata" not in layout_content:
                self.issues.append({
                    "type": "info",
                    "message": "Consider adding metadata to your root layout for better SEO.",
                    "file": "app/layout.tsx"
                })

    def check_package_json(self) -> None:
        """Check package.json for Next.js specific dependencies and scripts."""
        package_path = self.repo_path / "package.json"
        if not package_path.exists():
            self.issues.append({
                "type": "error",
                "message": "No package.json found.",
                "file": "package.json"
            })
            return

        try:
            with open(package_path, 'r') as f:
                package = json.load(f)

            # Check Next.js version
            next_version = package.get("dependencies", {}).get("next")
            if not next_version:
                self.issues.append({
                    "type": "error",
                    "message": "Next.js not found in dependencies.",
                    "file": "package.json"
                })
            elif next_version.startswith("12"):
                self.issues.append({
                    "type": "warning",
                    "message": "Using Next.js 12. Consider upgrading to a newer version for better features and performance.",
                    "file": "package.json"
                })

            # Check for recommended dependencies
            recommended = ["@vercel/analytics", "next-themes"]
            for dep in recommended:
                if dep not in package.get("dependencies", {}):
                    self.issues.append({
                        "type": "info",
                        "message": f"Consider adding {dep} for better functionality.",
                        "file": "package.json"
                    })

        except json.JSONDecodeError:
            self.issues.append({
                "type": "error",
                "message": "Invalid package.json format.",
                "file": "package.json"
            })

    def run_checks(self) -> List[Dict]:
        """Run all Next.js specific checks."""
        self.check_next_config()
        self.check_app_directory()
        self.check_package_json()
        return self.issues

def check_nextjs(repo_path: str) -> List[Dict]:
    """Main function to run Next.js checks."""
    checker = NextJSChecker(repo_path)
    return checker.run_checks()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_nextjs.py <repo_path>")
        sys.exit(1)
    
    issues = check_nextjs(sys.argv[1])
    print(json.dumps(issues, indent=2)) 