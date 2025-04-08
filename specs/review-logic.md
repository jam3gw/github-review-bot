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

### Next.js Specific
- App directory structure
- Image optimization settings
- Metadata configuration
- SWC minification
- Recommended dependencies
- TypeScript configuration
- Build settings

### Vercel Specific
- Deployment configuration
- Environment variables
- Build settings
- Analytics integration
- CLI setup
- Deployment files
- Performance optimization

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

### Next.js Configuration
⚠️ Missing image optimization
- Enable image optimization in next.config.js
- Consider using next/image component

### Vercel Deployment
✅ All deployment settings are correct
⚠️ Missing analytics integration
- Consider adding @vercel/analytics

### Documentation
❌ Missing docstrings in:
- api/endpoints.py
- utils/helpers.py

### Recommendations
1. Add input validation
2. Update documentation
3. Add unit tests
4. Enable image optimization
5. Add Vercel analytics
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
- Language-specific settings can be configured
- Framework-specific settings can be configured 