# Configuration

This document details how the GitHub Review Bot is configured.

## Configuration File

The bot is configured via `.github/bot-config.yml` in each repository:

```yaml
# Required: Repository type
type: default  # Options: default, ai_agent, api, frontend

# Required: Review strictness level
strictness: medium  # Options: low, medium, high

# Optional: Custom rules
rules:
  # Enable/disable specific checks
  code_style: true
  security: true
  documentation: true
  tests: true
  performance: true

  # Custom thresholds
  min_test_coverage: 80
  max_file_size_kb: 100
  max_complexity: 10

# Optional: Language-specific settings
python:
  # Python-specific checks
  use_black: true
  use_flake8: true
  use_bandit: true
  ignore_errors:
    - E501  # Line too long
    - W503  # Line break before binary operator

javascript:
  # JavaScript/TypeScript specific checks
  use_eslint: true
  use_prettier: true
  use_typescript: true
  ignore_rules:
    - "@typescript-eslint/no-explicit-any"
    - "no-console"

# Optional: AI Agent specific settings
ai_agent:
  # Model requirements
  min_model_version: "gpt-4"
  require_safety_checks: true
  validate_responses: true

# Optional: API specific settings
api:
  # API documentation requirements
  require_openapi: true
  validate_schema: true
  require_error_handling: true

# Optional: Frontend specific settings
frontend:
  # Frontend requirements
  require_typescript: true
  require_tests: true
  require_storybook: false

# Optional: Custom messages
messages:
  approval: "✅ All checks passed! Great work!"
  request_changes: "⚠️ Please address the following issues:"
  error: "❌ Critical issues found that must be fixed:"
```

## Configuration Loading

1. **Default Configuration**
   - Loaded from bot's default config
   - Provides baseline settings
   - Ensures minimum requirements

2. **Repository Configuration**
   - Loaded from `.github/bot-config.yml`
   - Overrides default settings
   - Validated against schema

3. **Environment Variables**
   - Can override specific settings
   - Useful for organization-wide defaults
   - Format: `BOT_CONFIG_<KEY>=<value>`

## Configuration Validation

1. **Schema Validation**
   - Validate YAML structure
   - Check required fields
   - Validate value types

2. **Value Validation**
   - Check valid options
   - Validate thresholds
   - Ensure compatibility

3. **Error Handling**
   - Log validation errors
   - Use defaults for invalid values
   - Notify repository admins

## Configuration Inheritance

1. **Organization Level**
   - Set in organization settings
   - Applies to all repositories
   - Can be overridden per repo

2. **Repository Level**
   - Set in `.github/bot-config.yml`
   - Overrides organization settings
   - Specific to repository

3. **PR Level**
   - Can be overridden in PR
   - Useful for testing
   - Temporary changes

## Security Considerations

1. **Sensitive Data**
   - Never store secrets in config
   - Use environment variables
   - Use GitHub secrets

2. **Access Control**
   - Validate config changes
   - Require admin approval
   - Log all changes

3. **Rate Limiting**
   - Configure API limits
   - Set check intervals
   - Handle rate limits

## Migration

1. **Version Updates**
   - Handle config changes
   - Provide migration guide
   - Support old formats

2. **Breaking Changes**
   - Announce in advance
   - Provide upgrade path
   - Maintain compatibility

3. **Deprecation**
   - Mark deprecated options
   - Provide alternatives
   - Remove in future versions 