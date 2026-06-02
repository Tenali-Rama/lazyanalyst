# Testing & Contributing Guide

## Testing

### Running Tests

LazyAnalyst uses pytest for testing. Make sure pytest is installed:

```bash
pip install pytest
```

#### Run All Tests

```bash
pytest tests/
```

#### Run Specific Test File

```bash
pytest tests/test_loader.py
```

#### Run Specific Test Function

```bash
pytest tests/test_loader.py::TestLoaderCSV::test_load_valid_csv
```

#### Run Tests with Verbose Output

```bash
pytest tests/ -v
```

#### Run Tests with Coverage Report

```bash
pip install pytest-cov
pytest tests/ --cov=lazyanalyst --cov-report=html
```

---

## Test Structure

Tests are organized by module:

```
tests/
├── __init__.py
├── test_loader.py       — Tests for CSV/Excel loading
├── test_schema.py       — Tests for column type detection
├── test_quality.py      — Tests for data quality auditing
└── test_analyze.py      — Tests for main pipeline
```

### Test Classes

Each test file contains test classes grouped by functionality:

**test_loader.py:**
- `TestLoaderCSV` — CSV file loading tests
- `TestLoaderExcel` — Excel file loading tests
- `TestLoaderErrors` — Error handling tests
- `TestDataTypeInference` — Data type detection tests

**test_schema.py:**
- `TestSchemaDetection` — Column type detection tests
- `TestSchemaEdgeCases` — Edge case handling tests
- `TestSchemaOutput` — Output format validation

**test_quality.py:**
- `TestQualityAudit` — Quality audit tests
- `TestQualityIssues` — Quality issue detection

**test_analyze.py:**
- `TestAnalyzePipeline` — Full pipeline tests
- `TestAnalyzeErrorHandling` — Error handling
- `TestAnalyzeResultObject` — Result object tests

---

## Writing New Tests

### Test Template

```python
import pytest
from lazyanalyst import module_name


class TestFeatureName:
    """Test description"""
    
    def setup_method(self):
        """Run before each test"""
        # Initialize test data
        pass
    
    def teardown_method(self):
        """Run after each test"""
        # Cleanup
        pass
    
    def test_specific_behavior(self):
        """Test description"""
        # Arrange
        test_input = ...
        
        # Act
        result = module_name.function(test_input)
        
        # Assert
        assert result == expected_output
```

### Best Practices

1. **Use descriptive test names** — Start with `test_` and describe what is tested
2. **One assertion per test** — Each test should verify one behavior
3. **Use setup/teardown** — Clean up temporary files and resources
4. **Test edge cases** — Empty data, nulls, duplicates, outliers
5. **Test error handling** — Verify proper exceptions are raised
6. **Use fixtures** — Create reusable test data in setup methods

---

## Contributing

### Fork & Clone

```bash
git clone https://github.com/yourusername/lazyanalyst.git
cd lazyanalyst
```

### Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### Make Changes

Follow the style rules from the spec:
- Use simple variable names (`df`, `val`, `res`, not `dataframe_result`)
- Mix naming styles (mostly snake_case, occasional camelCase)
- Write short comments explaining "why", not "what"
- Use one-line docstrings only
- Don't use type hints or dataclasses
- Import everything at the top

### Write Tests

For any new module or function:

```bash
# Create test file: tests/test_your_module.py
pytest tests/test_your_module.py
```

### Run All Tests

```bash
pytest tests/ -v
```

### Commit & Push

```bash
git add .
git commit -m "Add feature: brief description"
git push origin feature/your-feature-name
```

### Submit Pull Request

Create a PR on GitHub with:
- Clear description of changes
- Reference to any related issues
- Confirmation that all tests pass

---

## Code Style

LazyAnalyst code is intentionally written in a "junior developer" style:

### ✓ DO:
```python
# Simple variable names
df = pd.read_csv("file.csv")
val = df['column'].mean()

# Short docstrings
def load_file(path):
    """load csv file"""
    df = pd.read_csv(path)
    return df

# Simple comments
# using numpy for speed
result = np.array([1, 2, 3])

# Inconsistent formatting is OK
x = 1
y=2
z = 3
```

### ✗ DON'T:
```python
# Overly descriptive names
loaded_dataframe_from_csv_file = pd.read_csv(...)

# Type hints
def analyze(data: pd.DataFrame) -> dict:
    ...

# Complex docstrings
def load_file(path):
    """
    Load a CSV file from the given path.
    
    Args:
        path (str): The file path
    
    Returns:
        pd.DataFrame: The loaded dataframe
    """
```

---

## Module Overview

### loader.py
- `load(filepath)` — Load CSV/Excel into DataFrame
- Auto-detect delimiter (comma, semicolon, tab)
- Auto-detect encoding
- Infer column dtypes

**Test file:** `test_loader.py`

### schema.py
- `detect(df)` — Classify columns into 5 types
- Returns: `{column_name: type}` dictionary
- Types: numerical, categorical, datetime, boolean, identifier

**Test file:** `test_schema.py`

### quality.py
- `audit(df, schema)` — Assess data quality
- Returns: quality report with score, issues, missing values, duplicates, outliers

**Test file:** `test_quality.py`

### cleaner.py
- `clean(df, schema, quality_report)` — Auto-clean data
- Handle missing values, duplicates, outliers
- Returns: (cleaned_df, actions_list)

### eda.py
- `run(df, schema)` — Exploratory data analysis
- Compute statistics per column
- Returns: EDA results dictionary

### visualizer.py
- `generate(df, schema)` — Create PNG plots
- Histograms, distributions, heatmap
- Saves to `outputs/plots/`

### features.py
- `engineer(df, schema)` — Create new features
- Ratios, interactions, logarithmic, binning
- Returns: (df_with_features, features_list)

### stats.py
- `run(df, schema)` — Run statistical tests
- Correlations, t-tests, ANOVA, chi-square
- Returns: list of test results

### insights.py
- `generate(eda_results, stats_results, quality_report)` — Generate insights
- Plain English sentences from data patterns
- Returns: list of insight strings

### dashboard.py
- `build(inputs)` — Build interactive dashboard
- Plotly charts, dark theme
- Saves: `outputs/dashboard.html`

### reporter.py
- `build(inputs)` — Build comprehensive report
- Executive summary, tables, charts
- Saves: `outputs/report.html`

### analyze.py
- `analyze(filepath, dashboard, report)` — Main entry point
- Runs all 11 modules in sequence
- Returns: LazyAnalystResult object

---

## Debugging Tips

### Print Debugging
```python
# LazyAnalyst modules have print() statements
# View them when running the pipeline:
result = la.analyze("data.csv")
```

### Test with Sample Data
```python
import pandas as pd
import tempfile

# Create small test CSV
df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
df.to_csv('test.csv', index=False)

# Test your code
result = la.analyze('test.csv')
```

### Examine Intermediate Results
```python
result = la.analyze('data.csv')
cleaned = result.cleaned_data()
print(cleaned.info())
print(cleaned.describe())
```

---

## Common Issues

### Test Fails: "FileNotFoundError"
- Ensure your test uses `tempfile` and cleans up after
- Use `setup_method()` and `teardown_method()`

### Test Fails: "ModuleNotFoundError"
- Run tests from project root: `pytest tests/`
- Install package in dev mode: `pip install -e .`

### Tests Pass Locally, Fail in CI
- Make sure all files are tracked in git
- Check Python version compatibility (3.7+)
- Verify all dependencies in requirements

---

## Resources

- **Pytest docs**: https://docs.pytest.org/
- **Pandas docs**: https://pandas.pydata.org/docs/
- **NumPy docs**: https://numpy.org/doc/
- **SciPy docs**: https://docs.scipy.org/

---

## Getting Help

- Open an issue on GitHub
- Include error messages and dataset sample
- Provide steps to reproduce
- Share Python and package versions: `python --version && pip list`
