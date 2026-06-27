# AGENTS.md - AI Agent Integration Guide

This document describes how AI agents and automation tools interact with the QR Code Generator project.

## Overview

The QR Code Generator is designed to work seamlessly with AI agents, automation pipelines, and CI/CD systems. This guide helps integrate these tools effectively.

## GitHub Copilot / AI Assistant Integration

### Project Context

**Technology Stack:**
- Backend: Python 3.8+, Flask
- Frontend: HTML5, CSS3, JavaScript
- QR Library: qrcode library
- Testing: pytest
- Containerization: Docker, Docker Compose

**Project Structure:**
```
qr-code/
├── src/backend/       # Flask API
├── src/frontend/      # Web UI
├── tests/            # Test suite
├── docs/             # Documentation
└── generated/        # Output directory
```

### Quick Reference for Agents

#### Start Development Server
```bash
python src/backend/app.py  # Backend runs on http://localhost:5000
```

#### Run Tests
```bash
pytest
pytest --cov=src tests      # With coverage report
```

#### Run Code Quality Checks
```bash
ruff check src/             # Linting
mypy src/                   # Type checking
bandit -r src/              # Security scan
```

#### Build Docker Image
```bash
docker-compose up --build
```

#### Format Code
```bash
ruff format src/
```

## Automated Workflows

### Pre-commit Hooks

The project uses pre-commit hooks to maintain code quality:

```bash
pre-commit install
```

Pre-commit checks:
- Code formatting (Ruff)
- Type checking (Mypy)
- Security scanning (Bandit)
- Unused imports detection
- YAML validation

### CI/CD Pipeline

The project uses GitLab CI with the following stages:

1. **Lint & Format** - Code quality checks
2. **Type Check** - Type validation with Mypy
3. **Test** - Run test suite with coverage
4. **Build** - Build Docker image
5. **Deploy** - Deploy to staging/production

See `.gitlab-ci.yml` for pipeline configuration.

## API Endpoints for Automation

### Generate QR Code
```
POST /api/generate
Content-Type: application/json

{
  "data": "string",
  "size": "S|M|L|XL",
  "error_correction": "L|M|Q|H",
  "format": "png|svg|pdf",
  "color": "#RRGGBB",
  "background": "#RRGGBB"
}
```

### Batch Processing
```
POST /api/batch
Content-Type: multipart/form-data

file: CSV or JSON file
options: JSON configuration
```

### History Retrieval
```
GET /api/history
```

See [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full details.

## Testing for Agents

### Test Structure
```
tests/
├── test_api.py              # API endpoint tests
├── test_qr_generator.py     # QR generation tests
├── test_file_handler.py     # File handling tests
├── test_validator.py        # Input validation tests
└── conftest.py              # Shared fixtures
```

### Running Specific Tests
```bash
# Run single test file
pytest tests/test_qr_generator.py

# Run single test
pytest tests/test_qr_generator.py::test_simple_qr_generation

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=src --cov-report=html tests/
```

## Key Files for Modification

### Backend Logic
- `src/backend/app.py` - Main Flask application
- `src/backend/services/qr_generator.py` - QR generation logic
- `src/backend/routes/qr_routes.py` - API routes
- `src/backend/utils/validator.py` - Input validation

### Frontend
- `src/frontend/index.html` - Main HTML
- `src/frontend/js/app.js` - Client-side logic
- `src/frontend/css/style.css` - Styling

### Configuration
- `config.py` - Application settings
- `docker-compose.yml` - Docker setup
- `.gitlab-ci.yml` - CI/CD pipeline

## Code Quality Standards

### Type Hints
All functions should have type hints:
```python
def generate_qr(data: str, size: str = "M") -> bytes:
    """Generate QR code from data."""
    pass
```

### Documentation
All functions need docstrings:
```python
def generate_qr(data: str) -> bytes:
    """
    Generate a QR code from the provided data.
    
    Args:
        data: The data to encode in the QR code
        
    Returns:
        The QR code as bytes in PNG format
        
    Raises:
        ValueError: If data exceeds maximum length
    """
    pass
```

### Testing
- Minimum 80% code coverage
- All public functions tested
- Edge cases covered

## Security Considerations

### Input Validation
- All user inputs validated before processing
- File uploads restricted by size and type
- SQL injection prevention (though using JSON storage)

### Output Handling
- QR codes generated securely
- No sensitive data logging
- Temporary files cleaned up

### Dependencies
- Regular `pip-audit` checks
- Dependencies pinned in requirements.txt
- Security patches applied promptly

## Performance Optimization

### Caching
- Generated QR codes cached temporarily
- History stored in JSON (SQLite for production)

### Batch Processing
- Asynchronous processing for large batches
- Progress tracking via WebSocket/polling

### Resource Limits
- Maximum file size: 10MB (configurable)
- Batch timeout: 300 seconds (configurable)
- Maximum QR code data: 2953 bytes

## Troubleshooting for Agents

### Common Issues

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Test Failures**
```bash
# Run with verbose output
pytest -vv tests/

# Run specific test
pytest tests/test_name.py::function_name -vv
```

**Type Checking Issues**
```bash
# Check mypy version compatibility
mypy --version

# Force cache rebuild
mypy --cache-dir=/dev/null src/
```

**Docker Build Failures**
```bash
# Clean build
docker-compose down
docker-compose up --build

# Check logs
docker-compose logs -f
```

## Useful Commands Summary

```bash
# Development
python src/backend/app.py              # Start server
pytest                                 # Run tests
ruff check src/                        # Lint
mypy src/                              # Type check

# Code Quality
ruff format src/                       # Format code
bandit -r src/                         # Security scan
pip-audit                              # Check dependencies

# Docker
docker-compose up                      # Start services
docker-compose down                    # Stop services
docker-compose logs -f                 # View logs

# Git
git commit -m "feat: description"      # Conventional commit
git push origin feature/name           # Push branch
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Code style
- Testing requirements
- Pull request process
- Commit message format

## Support

For questions or issues:
1. Check [USER_MANUAL.md](../USER_MANUAL.md)
2. Review [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
3. Open an issue on GitLab

---

**Last Updated:** January 2024
