# Testing
The following describes how to run the tests for this project.

- Run all tests with the following command:
```bash
pytest -v
```
## Coverage
The following commands are run to describe test coverage over the code:

### Basic usage
```bash
pytest --cov=src
```
Runs tests and reports coverage for `src`.

### Show missing lines
```bash
pytest --cov=src --cov-report=term-missing
```
*Omit init files by including* `--cov-config=pytest.ini`

### Multiple packages/paths
```bash
pytest --cov=app --cov=core
```

### HTML report
```bash
pytest --cov=src --cov-report=html
```
Generates `htmlcov/index.html` — open it in a browser for a line-by-line view.

### XML report (for CI tools, e.g. SonarQube, Codecov)
```bash
pytest --cov=src --cov-report=xml
```

### Fail if coverage below threshold
```bash
pytest --cov=src --cov-fail-under=80
```

### Combine reports (term + html)
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

### Only show coverage for specific test run
```bash
pytest tests/test_module.py --cov=src
```

### Exclude files/dirs
Add to `.coveragerc` or `pyproject.toml`:
```ini
[coverage:run]
omit =
    */tests/*
    */migrations/*
```

### Append coverage across multiple runs (e.g. parallel test suites)
```bash
pytest --cov=src --cov-append
```

### Erase previous coverage data
```bash
coverage erase
```

### Branch coverage (not just line coverage)
```bash
pytest --cov=src --cov-branch
```