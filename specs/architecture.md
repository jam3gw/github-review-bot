# GitHub Review Bot Architecture

This document outlines how the GitHub Review Bot works as a GitHub Action.

## Implementation Overview

The bot runs entirely within GitHub's Actions infrastructure, triggered by PR events.

### Key Benefits
- No external hosting needed
- Simple setup process
- Runs in GitHub's secure infrastructure
- Direct access to repository contents
- Native integration with GitHub workflows

## Setup Instructions

### For Personal Repositories

1. **Create Action Configuration**
   Create `.github/workflows/code-review.yml` in your repository:
   ```yaml
   name: Code Review
   on:
     pull_request:
       types: [opened, synchronize, reopened]
   
   jobs:
     review:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: your-username/github-review-bot@main
           with:
             github-token: ${{ secrets.GITHUB_TOKEN }}
   ```

2. **Configure Bot Settings**
   Create `.github/bot-config.yml` in your repository:
   ```yaml
   # Basic configuration example
   review_type: default  # Options: default, ai_agent, api, frontend
   strictness: medium    # Options: low, medium, high
   ```

### For Organizations

1. **Organization-wide Setup**
   - Create a repository within your organization to host the action
   - Name suggestion: `org-name/github-review-bot`
   - Fork or copy the action code into this repository

2. **Enable Action in Organization Settings**
   - Go to Organization Settings > Actions > General
   - Enable "Allow all actions and reusable workflows"
   - Or specifically allow this action

3. **Repository Setup**
   For each repository that needs the bot:
   ```yaml
   name: Code Review
   on:
     pull_request:
       types: [opened, synchronize, reopened]
   
   jobs:
     review:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: org-name/github-review-bot@main
           with:
             github-token: ${{ secrets.GITHUB_TOKEN }}
   ```

## Personal GitHub Setup

1. **Create Action Repository**
   - Create a new repository: `github-review-bot`
   - Make it public (required for GitHub Actions)
   - Initialize with the bot's code

2. **Configure Action Metadata**
   Create `action.yml` in the root:
   ```yaml
   name: 'GitHub Review Bot'
   description: 'Automated code review for pull requests'
   inputs:
     github-token:
       description: 'GitHub token for API access'
       required: true
   runs:
     using: 'node20'
     main: 'dist/index.js'
   ```

3. **Personal Access Token (Optional)**
   If needed for additional permissions:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate new token with required permissions
   - Add token to repository secrets if needed

4. **Testing Your Action**
   - Create a test repository
   - Add the workflow file
   - Create a test PR to verify functionality

## Usage

1. **Basic Usage**
   Just create pull requests - the bot will automatically review them based on your configuration.

2. **Configuration Updates**
   Modify `.github/bot-config.yml` to adjust review behavior:
   ```yaml
   review_type: default
   strictness: medium
   checks:
     style: true
     security: true
     tests: true
     docs: true
   ```

3. **Workflow Customization**
   Adjust the workflow file to change when the bot runs:
   ```yaml
   on:
     pull_request:
       types: [opened, synchronize, reopened]
       branches:
         - main
         - develop
   ``` 