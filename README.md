# GitHub Review Bot

An automated code review bot for GitHub repositories that analyzes pull requests and enforces best practices.

## Features

- Automated code review for Python and JavaScript/TypeScript projects
- Configurable review strictness levels
- Specialized checks for AI agent and API repositories
- Data privacy compliance scanning
- Automatic PR approval for passing checks
- Detailed review summaries with recommendations

## Setup

### 1. Repository Configuration

Create a `.github/bot-config.yml` file in your repository with the following structure:

```yaml
repo_type: default  # Options: default, ai_agent, api, frontend
review_strictness: medium  # Options: low, medium, high

enabled_checks:
  code_style: true
  security: true
  performance: true
  test_coverage: true
  documentation: true

# AI-specific checks (only for ai_agent repos)
ai_checks:
  prompt_engineering: false
  model_versioning: false
  response_validation: false

# API-specific checks (only for api repos)
api_checks:
  openapi_validation: false
  error_handling: false
  rate_limiting: false
  authentication: false

# Data privacy compliance
data_privacy:
  pii_scan: true
  gdpr_compliance: true
  ccpa_compliance: true
```

### 2. PR Template

Add a `.github/PULL_REQUEST_TEMPLATE.md` file to your repository to specify review preferences:

```markdown
# Pull Request

## Description
<!-- Describe your changes in detail -->

## Type of Review
<!-- Select one of the following options by checking the appropriate box -->
- [ ] Bot review only (automated approval if all checks pass)
- [ ] Bot + human review (automated checks with human review)

## Changes Made
<!-- List the main changes in this PR -->

## Testing
<!-- Describe how you tested your changes -->

## Checklist
- [ ] I have tested my changes
- [ ] I have updated documentation if needed
- [ ] I have added tests if needed
- [ ] All automated checks pass
```

## Usage

1. Create a pull request in your repository
2. Select the desired review type in the PR template
3. The bot will automatically:
   - Analyze code changes
   - Run configured checks
   - Generate a review summary
   - Either approve the PR or leave comments for human review

## Checks Performed

### General Checks
- Code style (using Flake8, Black, ESLint)
- Security vulnerabilities (using Bandit)
- Test coverage
- Documentation completeness
- Performance issues

### AI Agent Repository Checks
- Prompt engineering best practices
- Model versioning and compatibility
- Response validation and safety

### API Repository Checks
- OpenAPI/Swagger specification validation
- Error handling completeness
- Rate limiting implementation
- Authentication and authorization

### Data Privacy Checks
- PII (Personally Identifiable Information) scanning
- GDPR compliance validation
- CCPA compliance validation

## Development

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/github-review-bot.git
   cd github-review-bot
   ```

2. Install dependencies using uv:
   ```bash
   pip install uv
   uv venv
   uv pip install -e .
   ```

### Project Structure

```
github-review-bot/
├── .github/
│   └── workflows/
│       └── code-review.yml
├── github_review_bot/
│   ├── __init__.py
│   ├── ai_checks.py
│   ├── api_checks.py
│   ├── generate_review.py
│   ├── load_config.py
│   ├── parse_review_preference.py
│   ├── post_comments.py
│   ├── privacy_checks.py
│   └── run_analysis.py
├── tests/
│   └── test_load_config.py
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
uv pip install pytest
pytest
```

### Adding New Checks

1. Create a new Python script in `.github/scripts/`
2. Update the configuration schema in `bot-config.yml`
3. Add the check to the appropriate analysis function in `run_analysis.py`
4. Update the review summary generation in `generate_review.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and feature requests, please create an issue in the GitHub repository. 