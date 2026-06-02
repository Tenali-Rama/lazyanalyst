# LazyAnalyst API Documentation

## Overview

LazyAnalyst is an automated data analysis library that performs comprehensive data analysis without requiring manual code. Simply point it to your dataset and it handles everything: cleaning, analysis, visualizations, statistical tests, and HTML reports.

---

## Installation

```bash
pip install lazyanalyst
```

**Requirements:**
- Python 3.7+
- pandas
- numpy
- scipy
- matplotlib
- seaborn
- plotly
- openpyxl (for Excel support)

---

## Quick Start

### Basic Usage

```python
import lazyanalyst as la

# Analyze a CSV or Excel file
result = la.analyze("your_data.csv")

# Open the interactive dashboard
result.dashboard()

# Open the HTML report
result.report()

# Access cleaned data as a DataFrame
cleaned_df = result.cleaned_data()
```

### Supported File Formats

- CSV files (`.csv`) — auto-detects delimiter and encoding
- Excel files (`.xlsx`)

---

## API Reference

### `analyze(filepath, dashboard=True, report=True)`

**Description:**
Runs the complete analysis pipeline on a dataset file.

**Parameters:**
- `filepath` (str): Path to CSV or Excel file
- `dashboard` (bool, optional): Generate interactive dashboard (default: True)
- `report` (bool, optional): Generate HTML report (default: True)

**Returns:**
- `LazyAnalystResult`: Result object with methods to access outputs

**Raises:**
- `FileNotFoundError`: If file does not exist
- `ValueError`: If file type is not supported

**Example:**
```python
# Full analysis with both dashboard and report
result = la.analyze("sales.csv")

# Analysis with only report
result = la.analyze("data.xlsx", dashboard=False)

# Analysis with no outputs (just clean the data)
result = la.analyze("raw_data.csv", dashboard=False, report=False)
```

---

## LazyAnalystResult Object

The object returned by `analyze()` provides methods to access analysis outputs.

### Methods

#### `dashboard()`

Opens the interactive dashboard in your default web browser.

**Example:**
```python
result = la.analyze("data.csv")
result.dashboard()  # Opens outputs/dashboard.html
```

#### `report()`

Opens the HTML report in your default web browser.

**Example:**
```python
result = la.analyze("data.csv")
result.report()  # Opens outputs/report.html
```

#### `cleaned_data()`

Returns the cleaned dataset as a pandas DataFrame.

**Returns:** pandas DataFrame

**Example:**
```python
result = la.analyze("data.csv")
cleaned_df = result.cleaned_data()
print(cleaned_df.head())
```

### Attributes

- `cleaned_data_path` (str): Path to cleaned CSV file
- `report_path` (str): Path to HTML report (or empty string if not generated)
- `dashboard_path` (str): Path to HTML dashboard (or empty string if not generated)

---

## Analysis Pipeline

LazyAnalyst runs 11 sequential modules on your data:

1. **Loader** — Load and parse CSV or Excel files
2. **Schema Detection** — Classify columns into types (numerical, categorical, datetime, boolean, identifier)
3. **Data Quality Audit** — Assess data quality, missing values, duplicates, outliers
4. **Cleaner** — Auto-clean data based on quality issues
5. **Exploratory Data Analysis** — Compute statistical summaries
6. **Visualizer** — Generate histograms, distributions, heatmaps
7. **Feature Engineering** — Create derived features (ratios, interactions)
8. **Statistical Tests** — Run correlation and hypothesis tests
9. **Insights** — Generate plain-English business insights
10. **Dashboard** — Build interactive visualization dashboard
11. **Reporter** — Generate formatted HTML report

### Column Type Detection

LazyAnalyst automatically detects 5 column types:

| Type | Detection Rule | Example |
|------|---|---|
| **numerical** | Integer or float values | age, salary, count |
| **categorical** | Text values or <20 unique values | color, department, status |
| **datetime** | Date/time format or date-related column name | date, timestamp, signup_date |
| **boolean** | Only 2 unique values | is_active, has_error, True/False |
| **identifier** | Column name contains "id/code/key" or all unique values | customer_id, product_code |

---

## Output Files

All outputs are saved to the `outputs/` folder created automatically on first run.

### Generated Files

- `outputs/report.html` — Comprehensive HTML report with all analysis
- `outputs/dashboard.html` — Interactive dashboard with charts
- `outputs/cleaned_data.csv` — Cleaned version of your dataset
- `outputs/insights.txt` — Plain-English insights (one per line)
- `outputs/plots/` — Directory containing chart images
  - `heatmap.png` — Correlation heatmap
  - `distributions.png` — Distribution plots

---

## Dashboard Features

The interactive dashboard includes:

1. **Overview** — Dataset summary (size, columns, quality score)
2. **Data Quality** — Missing values, duplicates, outliers
3. **Distributions** — Histograms for numerical columns, bar charts for categorical
4. **Correlations** — Interactive correlation heatmap
5. **Statistical Tests** — Summary table of all tests run
6. **Insights** — List of automatically generated insights

---

## Report Features

The HTML report includes:

1. **Executive Summary** — High-level overview and top insights
2. **Dataset Overview** — Table of all columns and their types
3. **Data Quality** — Quality score, issues found, cleaning actions
4. **Exploratory Analysis** — Statistical summaries (mean, median, std, etc.)
5. **Visualizations** — All generated charts and plots
6. **Statistical Results** — Details of all hypothesis tests
7. **Feature Engineering** — List of new features created
8. **Insights** — Business insights generated from data

---

## Error Handling

LazyAnalyst is designed to be resilient. If any module fails:

- An error message is printed (not a crash)
- The pipeline continues with the next module
- Downstream modules work with empty results from failed modules

**Example output:**
```
[LazyAnalyst] Step 1/11 — Loading dataset...
[LazyAnalyst] Warning: loader failed — File not found. Skipping this step.
```

---

## Examples

### Example 1: Analyze Sales Data

```python
import lazyanalyst as la

# Load and analyze
result = la.analyze("sales.csv")

# View dashboard
result.dashboard()

# Get cleaned data
df = result.cleaned_data()
print(f"Analyzed {len(df)} sales records")
```

### Example 2: Data Quality Report Only

```python
import lazyanalyst as la

# Generate only report, skip dashboard
result = la.analyze("customer_data.csv", dashboard=False)
result.report()
```

### Example 3: Process Multiple Files

```python
import lazyanalyst as la
import os

# Analyze all CSV files in a folder
for file in os.listdir("data/"):
    if file.endswith(".csv"):
        result = la.analyze(f"data/{file}")
        print(f"✓ Analyzed {file}")
```

### Example 4: Programmatic Access

```python
import lazyanalyst as la

result = la.analyze("data.csv")

# Get cleaned data for further analysis
cleaned_df = result.cleaned_data()

# Perform custom analysis
print(cleaned_df.describe())
print(cleaned_df.corr())
```

---

## Supported Data Types

### Numerical Columns
- Integers
- Floats
- Auto-detected when dtype is int or float

### Categorical Columns
- Text values
- Detected when dtype is 'object' or <20 unique values

### DateTime Columns
- Date formats (YYYY-MM-DD, etc.)
- Timestamp formats
- Column names containing 'date', 'time', 'year', 'month'

### Boolean Columns
- True/False values
- 0/1 values
- Yes/No values

### Identifier Columns
- Column names containing 'id', 'code', 'key'
- All unique values

---

## Data Cleaning

LazyAnalyst automatically cleans data by:

1. **Handling Missing Values**
   - Drops rows with >50% missing values
   - Fills numerical columns with median
   - Drops categorical columns with high missing rate

2. **Removing Duplicates**
   - Detects and removes complete duplicate rows

3. **Outlier Treatment**
   - Flags outliers (IQR method for numerical columns)
   - Can cap values or remove rows with extreme outliers

4. **Type Conversion**
   - Auto-infers and converts column dtypes
   - Handles mixed-type columns gracefully

---

## Statistical Tests

LazyAnalyst automatically runs relevant statistical tests:

- **Correlation Analysis**: Pearson and Spearman correlations
- **Hypothesis Tests**: T-tests, ANOVA for group differences
- **Chi-Square Tests**: For categorical associations
- **Significance Level**: α = 0.05

All p-values and test results are included in the report and dashboard.

---

## Feature Engineering

LazyAnalyst automatically creates:

- **Ratios** — For pairs of numerical columns (e.g., cost per unit)
- **Interactions** — For selected numerical pairs
- **Logarithmic** — For skewed numerical distributions
- **Binning** — For continuous numerical columns (quartiles)

---

## Performance Considerations

- **File Size**: Tested up to ~100MB CSV files
- **Columns**: Handles 50+ columns efficiently
- **Rows**: Optimized for datasets up to 1M rows
- **Charts**: Browser performance depends on system; avoid >500K rows for smooth dashboard

---

## Troubleshooting

### Issue: "FileNotFoundError: Could not find file"
**Solution:** Verify the file path is correct and file exists.

### Issue: "ValueError: Only supports .csv and .xlsx files"
**Solution:** Convert your file to CSV or Excel format.

### Issue: Dashboard or report opens but shows no data
**Solution:** Check that `outputs/` folder exists and contains the HTML file. Try reopening the file.

### Issue: Analysis runs very slowly
**Solution:** For large files (>100MB), consider filtering to relevant columns first using a spreadsheet application.

---

## Limitations & Known Issues

- **Excel sheets**: Currently reads only the first sheet
- **Encoding**: CSV encoding is auto-detected; unusual encodings may need manual handling
- **Very high cardinality**: Categorical columns with >1000 unique values are treated as identifiers
- **Special characters**: File paths with special characters should be enclosed in quotes

---

## Advanced Configuration

LazyAnalyst doesn't currently support configuration files. For custom analysis, use the cleaned data:

```python
import lazyanalyst as la

# Get cleaned data
result = la.analyze("data.csv")
df = result.cleaned_data()

# Perform custom analysis
import pandas as pd
import matplotlib.pyplot as plt

# Your custom code here
df.groupby('category')['value'].mean().plot()
plt.show()
```

---

## Version

- **Current Version**: 1.0.0
- **Python Support**: 3.7+
- **Last Updated**: June 2024
