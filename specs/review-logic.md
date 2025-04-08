# Core Review Logic

This document outlines how the GitHub Review Bot performs code reviews.

## Review Process

1. **Trigger**
   - PR opened
   - PR synchronized (new commits)
   - PR reopened

2. **Configuration Loading**
   - Load repository-specific config from `.github/bot-config.yml`
   - Apply defaults for missing values

3. **Analysis**
   - Check repository type (default, ai_agent, api, frontend)
   - Run appropriate checks based on type
   - Collect results and metrics

4. **Review Generation**
   - Format results into readable review
   - Add recommendations
   - Determine approval status

5. **Review Posting**
   - Post review comments
   - Approve/request changes based on results
   - Update PR status checks

## Check Types

### General Checks
- Code style (flake8, black, eslint)
- Security vulnerabilities (bandit)
- Test coverage
- Documentation completeness
- Performance issues

### AI Agent Specific
- Prompt engineering best practices
- Model versioning and compatibility
- Response validation and safety

### API Specific
- OpenAPI/Swagger validation
- Error handling completeness
- Rate limiting implementation
- Authentication and authorization

### Frontend Specific
- TypeScript type checking
- ESLint rules
- Prettier formatting
- Build verification

## Review Output

### Review Comments
```markdown
## Code Review Results

### Code Style
✅ All files follow style guidelines

### Security
⚠️ Potential SQL injection in database.py
- Line 42: Use parameterized queries
- Line 87: Validate user input

### Documentation
❌ Missing docstrings in:
- api/endpoints.py
- utils/helpers.py

### Recommendations
1. Add input validation
2. Update documentation
3. Add unit tests
```

### PR Status
- ✅ All checks pass: Auto-approve
- ⚠️ Some issues: Request changes
- ❌ Major issues: Request changes with detailed comments

## Configuration Impact

### Review Strictness
- **Low**: Only critical issues
- **Medium**: All issues with recommendations
- **High**: All issues, must be fixed

### Enabled Checks
- Each check can be enabled/disabled
- Checks can be configured per repository type
- Custom rules can be added 