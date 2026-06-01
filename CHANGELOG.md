# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-06-01

### Added
- Initial release of LazyAnalyst
- Full automated data analysis pipeline
- CSV and XLSX file support
- 11 integrated analysis modules
- Interactive HTML dashboard with Plotly
- Professional HTML report generation
- Automated statistical testing framework
- Data quality auditing and reporting
- Feature engineering capabilities
- Exploratory data analysis (EDA)
- Natural language insights generation
- Data cleaning and preprocessing automation

### Modules Included
1. **loader.py** — File loading and dtype inference
   - Supports CSV (auto-detects encoding and delimiter)
   - Supports XLSX (Excel workbooks)
   - Automatic data type conversion

2. **schema.py** — Column type detection
   - Detects: numerical, categorical, datetime, boolean, identifier
   - Priority-based classification

3. **quality.py** — Data quality auditing
   - Missing value analysis
   - Duplicate detection
   - Outlier flagging
   - Quality score calculation

4. **cleaner.py** — Automated data cleaning
   - Missing value imputation
   - Duplicate removal
   - Outlier handling
   - Type conversion

5. **eda.py** — Exploratory data analysis
   - Descriptive statistics
   - Distribution analysis
   - Correlation analysis

6. **visualizer.py** — Chart generation
   - Histograms and distributions
   - Bar charts for categories
   - Scatter plots
   - Correlation heatmaps
   - PNG output with matplotlib/seaborn

7. **features.py** — Feature engineering
   - Polynomial features
   - Interaction terms
   - Normalization/scaling
   - Log transforms

8. **stats.py** — Statistical testing
   - Pearson/Spearman correlation
   - Independent T-tests
   - ANOVA
   - Chi-Square tests
   - P-value calculation and interpretation

9. **insights.py** — Automated insights
   - Correlation insights
   - Group difference insights
   - Data quality insights
   - Distribution insights
   - Natural language output

10. **dashboard.py** — Interactive dashboard
    - Plotly-based visualizations
    - Dark theme design
    - 6 main sections (Overview, Quality, Distributions, Correlations, Tests, Insights)
    - Self-contained HTML file
    - No server required

11. **reporter.py** — HTML report generation
    - Executive summary
    - Dataset overview
    - Data quality metrics
    - EDA statistics
    - Visualization embeddings
    - Statistical results
    - Actionable insights
    - Professional styling with print support

### Features
- One-line API: `dp.analyze("file.csv")`
- Automatic error handling and resilience
- Progress reporting throughout pipeline
- Comprehensive output documentation
- Browser-based results viewing
- No manual configuration required

### Documentation
- Comprehensive README with quick start guide
- Installation instructions via pip
- Full API reference
- Example usage patterns
- Architecture documentation
- Contributing guidelines

### License
- MIT License for open distribution
- Free for personal and commercial use

---

## Release Notes

### v1.0.0 Highlights
- One-liner analysis: `dp.analyze("data.csv")`
- 11 fully integrated modules
- Professional HTML outputs (dashboard + report)
- Automatic statistical testing
- Natural language insights
- Beautiful dark theme interface
- Fast processing even on moderate datasets
- Robust error handling

### What's Coming in v1.1
- Time series analysis module
- Anomaly detection
- Clustering analysis
- Advanced feature selection
- Custom analysis templates
- Export to PDF
- Interactive Jupyter notebook support

### Known Limitations
- Dashboard rendering requires modern browser
- Large files (>1GB) may require increased memory
- Some advanced statistical tests not included
- ML models use only sklearn basics

---

## Installation & Usage

### Install
```bash
pip install lazyanalyst
```

### Basic Usage
```python
import lazyanalyst as dp

result = dp.analyze("sales.csv")
result.dashboard()  # View interactive dashboard
result.report()      # View HTML report
```

### Supported Formats
- CSV (comma, semicolon, or tab-separated)
- XLSX (Excel workbooks)

---

## Changelog Format

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for security fix announcements

---

**For more information, visit the GitHub repository or PyPI page.**
