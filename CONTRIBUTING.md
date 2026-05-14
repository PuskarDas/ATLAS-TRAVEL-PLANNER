# Contributing to AI-Powered Group Travel Planner

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/AI-Group-Travel-Planner.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up development environment: See README for setup instructions

## Development Workflow

### Code Style
- Python: Follow PEP 8 (enforced by Black and Flake8)
- JavaScript/React: Follow ESLint configuration
- Run formatters before committing:
  ```bash
  # Python
  black .
  isort .
  
  # JavaScript
  npm run format
  ```

### Testing
- Write tests for new features
- Ensure all tests pass: `pytest tests/`
- Maintain >80% code coverage

### Commit Messages
- Use clear, descriptive commit messages
- Format: `type(scope): description`
- Examples:
  - `feat(recommendation): add new recommendation algorithm`
  - `fix(auth): resolve JWT validation issue`
  - `docs(api): update API documentation`

### Pull Request Process
1. Update README if adding new features
2. Update documentation
3. Ensure all tests pass
4. Submit PR with description of changes
5. Address review comments

## Reporting Issues

- Check if issue already exists
- Provide clear description and reproduction steps
- Include environment details
- Attach screenshots/logs if relevant

## Questions?

Feel free to open an issue or contact the maintainers.
