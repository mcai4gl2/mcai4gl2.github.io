# Development Guidelines for Image Optimizer

This document outlines the requirements and guidelines for developing and maintaining the Image Optimizer utility for Hugo blogs.

## 1. Python Environment Requirements

### DevContainer Setup
- **All Python development MUST be done inside the DevContainer**
- The DevContainer is configured with:
  - Python 3.11
  - Required dependencies (Pillow, numpy, click, tqdm, pytest)
  - Image optimizer package installed in development mode
  - VS Code Python extension for IntelliSense

### Local Development
- Do NOT install Python packages locally on the host machine
- Use the DevContainer for all Python-related development
- The DevContainer automatically mounts your workspace and syncs changes

## 2. Unit Testing Requirements

### Test Execution Environment
- **All unit tests MUST be run inside the DevContainer**
- Tests should be executed using pytest:
  ```bash
  python3 -m pytest tests/ -v
  ```

### Test Coverage
- **Minimum test coverage: 80%**
- Coverage is automatically checked in CI/CD pipeline
- To check coverage:
  ```bash
  python3 -m pytest tests/ --cov=image_optimizer --cov-report=term-missing
  ```

### Test Structure
- Unit tests are located in the `tests/` directory
- Test files follow the naming convention: `test_*.py`
- Test classes follow the naming convention: `Test*`
- Test methods follow the naming convention: `test_*`

## 3. Code Change Requirements

### Before Making Changes
1. Ensure DevContainer is running and up-to-date
2. Run existing tests to verify they pass
3. Check current test coverage

### After Making Changes
1. **ALL Python code changes MUST have corresponding unit tests**
2. Run the complete test suite:
   ```bash
   python3 -m pytest tests/ -v --cov=image_optimizer --cov-fail-under=80
   ```
3. Verify test coverage is at least 80%
4. Fix any failing tests before committing

### Test Coverage Guidelines
- New functions/methods should have dedicated unit tests
- Edge cases and error conditions must be tested
- Use parameterized tests for multiple input scenarios
- Mock external dependencies when necessary

## 4. Development Workflow

### Making Changes
1. Open the project in VS Code with DevContainer
2. Make your changes to the Python code
3. Write or update unit tests
4. Run tests with coverage check
5. Fix any issues until all tests pass with 80%+ coverage
6. Commit changes

### Running Tests
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run tests with coverage
python3 -m pytest tests/ --cov=image_optimizer --cov-report=term-missing

# Run specific test file
python3 -m pytest tests/test_utils.py -v

# Run tests with 80% coverage requirement
python3 -m pytest tests/ --cov=image_optimizer --cov-fail-under=80
```

### CI/CD Integration
- GitHub Actions automatically run tests in the DevContainer
- Tests are executed across multiple Python versions
- Coverage reports are uploaded to Codecov
- Pull requests must pass all tests before merging

## 5. Project Structure

```
image_optimizer/
├── __init__.py          # Package initialization with lazy imports
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── processor.py         # Core image processing logic
├── batch.py             # Batch processing engine
└── cli.py               # Command-line interface

tests/
├── __init__.py
├── test_config.py       # Configuration tests
├── test_utils.py        # Utility function tests
├── test_processor.py    # Image processor tests
├── test_batch.py        # Batch processor tests
└── test_cli.py          # CLI interface tests
```

## 6. Best Practices

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Document public functions and classes
- Keep functions focused and small

### Testing Best Practices
- Write descriptive test names
- Use AAA pattern (Arrange, Act, Assert)
- Test both positive and negative cases
- Keep tests independent and isolated
- Use fixtures for common test setup

### DevContainer Usage
- Rebuild DevContainer when dependencies change
- Use the integrated terminal for all Python commands
- Leverage VS Code extensions for better development experience

## 7. Troubleshooting

### Common Issues
- **ModuleNotFoundError**: Ensure you're in the DevContainer
- **Test failures**: Check that all dependencies are installed
- **Coverage below 80%**: Add tests for uncovered code paths

### Getting Help
- Check the GitHub Actions logs for CI/CD issues
- Review test output for specific failure details
- Ensure DevContainer is properly configured

## 8. Enforcement

These requirements are enforced through:
- GitHub Actions workflows that run tests in DevContainer
- Coverage checks that fail builds below 80%
- Code review process to ensure compliance
- Automated linting and formatting checks

Non-compliance with these guidelines will result in failed builds and blocked pull requests.