# LazyAnalyst v1.0.0

**Automated data analysis library for Python**

LazyAnalyst is an end-to-end data analysis library that automates everything you'd do manually with Pandas and NumPy. Load a dataset, run one line of code, and get a complete analysis with insights, visualizations, statistical tests, and a professional HTML report.

## Quick Start

```python
import lazyanalyst as dp

# Analyze any CSV or Excel file
result = dp.analyze("sales_data.csv")

# Open the interactive dashboard
result.dashboard()

# Or view the professional report
result.report()
```

That's it! LazyAnalyst handles:
- Automated data loading and type detection
- Data quality auditing and reporting
- Intelligent data cleaning
- Exploratory data analysis
- Statistical testing (Pearson, Spearman, ANOVA, Chi-Square)
- Feature engineering
- Interactive Plotly dashboard
- Professional HTML report generation
- Automated insights and interpretations

## Installation

Install via pip:

```bash
pip install lazyanalyst
```

**Requirements:** Python 3.8+

Or install from source:

```bash
git clone https://github.com/Tenali-Rama/lazyanalyst.git
cd lazyanalyst
pip install -e .
```

## Features

### 1. **Automated Pipeline**
No configuration needed. Just provide a CSV or Excel file and LazyAnalyst handles the rest.

### 2. **Data Quality Auditing**
Automatically detects:
- Missing values
- Duplicate rows
- Outliers
- Data type inconsistencies
- Quality score calculation

### 3. **Intelligent Cleaning**
- Auto-detects and fixes common issues
- Handles missing values intelligently
- Removes duplicates
- Converts data types automatically

### 4. **Exploratory Data Analysis (EDA)**
- Summary statistics (mean, median, std, min, max)
- Distribution analysis
- Correlation detection
- Categorical value counts

### 5. **Statistical Testing**
Runs appropriate tests automatically:
- **Pearson/Spearman Correlation** for numerical relationships
- **Independent T-Test** for 2-group comparisons
- **ANOVA** for 3+ group comparisons
- **Chi-Square** for categorical relationships

### 6. **Feature Engineering**
- Polynomial features
- Interaction terms
- Scaled/normalized versions
- Log transforms for skewed data

### 7. **Visualizations**
Generates:
- Distribution histograms
- Categorical bar charts
- Correlation heatmaps
- Scatter plots for relationships

### 8. **Interactive Dashboard**
Beautiful, self-contained HTML dashboard with all analyses and charts.

### 9. **Professional Report**
PDF-ready HTML report with executive summary, findings, and visualizations.

## Example Usage

### Basic Analysis
```python
import lazyanalyst as dp

result = dp.analyze("data.csv")
result.dashboard()  # Open interactive dashboard
result.report()      # Open HTML report
```

### With Options
```python
result = dp.analyze("data.xlsx", dashboard=True, report=True)

# Access cleaned data
cleaned_df = result.cleaned_data()
```

### Supported File Types
- CSV (auto-detects encoding and delimiter)
- XLSX (Excel workbooks)

## Output Files

LazyAnalyst creates an `outputs/` folder with:

- `cleaned_data.csv` — Your cleaned dataset
- `report.html` — Professional report
- `dashboard.html` — Interactive dashboard
- `insights.txt` — Text summary of insights
- `plots/` — All generated visualizations

## Architecture

LazyAnalyst consists of 11 integrated modules:

1. **loader.py** — File loading with auto type inference
2. **schema.py** — Column type detection
3. **quality.py** — Data quality auditing
4. **cleaner.py** — Automated data cleaning
5. **eda.py** — Exploratory data analysis
6. **visualizer.py** — Chart generation
7. **features.py** — Feature engineering
8. **stats.py** — Statistical testing
9. **insights.py** — Natural language insights
10. **dashboard.py** — Interactive dashboard generation
11. **reporter.py** — HTML report generation

## Documentation

Full documentation available in the GitHub repository.

## License

MIT License - See LICENSE file for details

## Troubleshooting

### "FileNotFoundError"
- Check file path is correct
- Use absolute path if relative path doesn't work

### "ValueError: unsupported file type"
- Ensure file is .csv or .xlsx

### Dashboard won't open
- Check plotly and dash are installed
- Try opening dashboard.html directly in browser

## Support

For questions or issues, check this README or the GitHub repository.

---

Transform your data analysis workflow with one line of code.
