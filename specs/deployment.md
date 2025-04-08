# GitHub Review Bot Deployment

This document outlines how to deploy and maintain the GitHub Review Bot as a GitHub Action.

## Deployment Overview

The bot is deployed as a GitHub Action that runs in response to pull request events. There are two main deployment scenarios:

1. **Personal Repository Deployment**
   - For individual developers or small projects
   - Single repository setup
   - Quick and simple configuration

2. **Organization-wide Deployment**
   - For teams and organizations
   - Centralized reusable workflow
   - Consistent review standards across repositories
   - No need to duplicate workflow files

## Installation Steps

### Personal Repository Setup

1. **Add Workflow File**
   Create `.github/workflows/code-review.yml`:
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
   Create `.github/bot-config.yml`:
   ```yaml
   review_type: default
   strictness: medium
   checks:
     style: true
     security: true
     tests: true
     docs: true
   ```

### Organization Setup

1. **Create Central Workflow Repository**
   - Create `org-name/github-review-bot`
   - Make it public
   - Add the reusable workflow:

   `.github/workflows/review.yml`:
   ```yaml
   name: Code Review
   on:
     workflow_call:
       inputs:
         config_path:
           required: false
           type: string
           default: '.github/bot-config.yml'
       secrets:
         GITHUB_TOKEN:
           required: true
   
   jobs:
     review:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: org-name/github-review-bot@main
           with:
             github-token: ${{ secrets.GITHUB_TOKEN }}
             config-path: ${{ inputs.config_path }}
   ```

2. **Enable Action in Organization**
   - Go to Organization Settings > Actions > General
   - Enable "Allow all actions and reusable workflows"
   - Or specifically allow this workflow

3. **Repository Integration Options**

   Option 1: **Automatic Organization-wide Deployment**
   - Create an organization-level workflow in `.github` repository:
   ```yaml
   # .github/.github/workflows/org-review.yml
   name: Organization Code Review
   on:
     pull_request:
       types: [opened, synchronize, reopened]
   
   jobs:
     review:
       uses: org-name/github-review-bot/.github/workflows/review.yml@main
       secrets: inherit
   ```
   This will automatically apply to all repositories in the organization.

   Option 2: **Opt-in Repository Deployment**
   For repositories that want to use the workflow:
   ```yaml
   # Only needed in repositories that want to opt-in
   name: Code Review
   on:
     pull_request:
       types: [opened, synchronize, reopened]
   
   jobs:
     review:
       uses: org-name/github-review-bot/.github/workflows/review.yml@main
       secrets: inherit
   ```

   Both options only require the `.github/bot-config.yml` in each repository for customization:
   ```yaml
   review_type: default
   strictness: medium
   checks:
     style: true
     security: true
     tests: true
     docs: true
   ```

## Action Configuration

### Required Settings

1. **GitHub Token**
   - Automatically provided by GitHub Actions
   - No additional setup needed
   - Has access to repository contents and PR management

2. **Repository Configuration**
   - Stored in `.github/bot-config.yml`
   - Controls review behavior and checks
   - Can be customized per repository

### Optional Settings

1. **Branch Filtering**
   ```yaml
   on:
     pull_request:
       types: [opened, synchronize, reopened]
       branches:
         - main
         - develop
   ```

2. **Schedule**
   ```yaml
   on:
     schedule:
       - cron: '0 0 * * *'  # Daily at midnight
   ```

## Maintenance

1. **Action Updates**
   - Update workflow version in central repository
   - Changes automatically propagate to all repositories
   - Test changes in a test repository before updating main branch

2. **Configuration Updates**
   - Modify `.github/bot-config.yml` in individual repositories
   - Create organization-wide default config in `.github` repository
   - Changes take effect on next PR

3. **Monitoring**
   - Check GitHub Actions logs
   - Review PR comments and status
   - Monitor action execution time
   - View organization-wide usage in Actions dashboard

## Troubleshooting

1. **Action Not Running**
   - Check organization permissions
   - Verify workflow references are correct
   - Ensure repository has Actions enabled
   - Check if repository is using correct workflow version

2. **Configuration Issues**
   - Validate YAML syntax
   - Check for required fields
   - Verify file permissions
   - Ensure config file is in correct location

3. **Permission Problems**
   - Ensure GitHub token has required permissions
   - Check organization settings
   - Verify repository access
   - Confirm workflow permissions are properly set 