# Getting Started with LazyAnalyst

Welcome to LazyAnalyst! This guide will help you get started with automated data analysis in just a few minutes.

## Installation

### 1. Install Python

Make sure you have Python 3.7 or newer installed. Check your version:

```bash
python --version
```

### 2. Install LazyAnalyst

```bash
pip install lazyanalyst
```

This will install LazyAnalyst and all required dependencies:
- pandas
- numpy
- scipy
- matplotlib
- seaborn
- plotly
- openpyxl

---

## Your First Analysis

### Step 1: Prepare Your Data

LazyAnalyst works with CSV and Excel files. Here's a simple example:

**sales_data.csv:**
```
date,region,product,sales,quantity
2024-01-01,North,ProductA,5000,100
2024-01-01,South,ProductB,3500,75
2024-01-02,North,ProductA,5200,105
2024-01-02,East,ProductC,4100,82
...
```

### Step 2: Write the Analysis Code

Create a Python file `analyze_sales.py`:

```python
import lazyanalyst as la

# Run analysis
result = la.analyze("sales_data.csv")

# View results
result.dashboard()
result.report()
```

### Step 3: Run the Analysis

```bash
python analyze_sales.py
```

LazyAnalyst will:
1. Load your data
2. Detect column types
3. Audit data quality
4. Clean the data
5. Run statistical analysis
6. Generate insights
7. Create a dashboard and report

Output:
```
[LazyAnalyst] Step 1/11 — Loading dataset...
Loaded 365 rows x 4 columns

[LazyAnalyst] Step 2/11 — Detecting schema...
date: datetime
region: categorical
product: categorical
sales: numerical
quantity: numerical

[LazyAnalyst] Step 3/11 — Auditing data quality...
Quality score: 95/100

[LazyAnalyst] Step 4/11 — Cleaning dataset...
Removed 2 duplicate rows
Filled 1 missing value

...

[LazyAnalyst] Analysis complete!
Outputs saved to ./outputs/
```

---

## Output Files

After analysis, check the `outputs/` folder:

```
outputs/
├── report.html          ← Open in browser for full report
├── dashboard.html       ← Open in browser for interactive dashboard
├── cleaned_data.csv     ← Cleaned version of your data
├── insights.txt         ← Text file with all insights
└── plots/
    ├── distributions.png
    └── heatmap.png
```

---

## Understanding Your Results

### The Dashboard

The interactive dashboard shows:

1. **Overview** — Dataset summary and quality score
2. **Data Quality** — Missing values and outliers
3. **Distributions** — Histograms and bar charts
4. **Correlations** — Interactive correlation heatmap
5. **Statistical Tests** — Test results and significance
6. **Insights** — Auto-generated business insights

### The Report

The HTML report includes:

1. **Executive Summary** — Key findings at a glance
2. **Data Quality Assessment** — Detailed quality analysis
3. **Exploratory Analysis** — Statistical summaries
4. **Visualizations** — Charts and plots
5. **Statistical Tests** — Full test results
6. **Insights** — Business insights and recommendations

### Insights

LazyAnalyst generates insights like:

```
▸ age has a strong positive correlation with salary (r=0.87)
▸ Department has a statistically significant effect on salary
▸ Product has 15% missing values — consider reviewing this column
▸ Sales is highly right-skewed. A log transform may be useful.
```

---

## Common Use Cases

### Sales Analysis

```python
import lazyanalyst as la

result = la.analyze("sales.csv")
result.dashboard()  # View sales trends, regional performance
result.report()     # Download full analysis
```

**Typical findings:**
- Top selling regions/products
- Revenue trends and seasonality
- Customer segment performance
- Price sensitivity correlations

### Customer Analytics

```python
import lazyanalyst as la

result = la.analyze("customers.csv")
result.report()
```

**Typical findings:**
- Customer segment characteristics
- Churn risk factors
- Purchase pattern analysis
- Demographics and behavior correlations

### Scientific Data

```python
import lazyanalyst as la

result = la.analyze("experiment_results.csv")
result.dashboard()
```

**Typical findings:**
- Distribution of measurements
- Statistical significance of differences
- Correlations between variables
- Outliers and anomalies

### Financial Data

```python
import lazyanalyst as la

result = la.analyze("financial_data.csv")
result.report()
```

**Typical findings:**
- Revenue and expense analysis
- Profit margin trends
- Cost correlations
- Anomaly detection

---

## Accessing Cleaned Data

Sometimes you need to do custom analysis on the cleaned data:

```python
import lazyanalyst as la
import matplotlib.pyplot as plt

# Run analysis
result = la.analyze("data.csv")

# Get cleaned DataFrame
df = result.cleaned_data()

# Custom analysis
print(df.describe())
print(df.groupby('category')['value'].mean())

# Create custom plots
df.plot(x='date', y='value')
plt.show()
```

---

## Data Requirements

### Supported File Formats

- **CSV files** — Comma, semicolon, or tab separated
- **Excel files** — `.xlsx` format (uses first sheet)

### Column Requirements

LazyAnalyst can handle:
- **Numerical columns** — integers, decimals
- **Text columns** — names, categories, descriptions
- **Dates** — various date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
- **Boolean** — True/False, Yes/No, 0/1
- **IDs** — customer_id, product_code, etc.

### Data Limits

- ✓ Works well with datasets up to 1 million rows
- ✓ Handles 50+ columns
- ✓ Tolerates missing values
- ✓ Handles duplicates automatically
- ✓ Detects and flags outliers

---

## Tips & Tricks

### 1. Excel Files with Multiple Sheets

LazyAnalyst reads the first sheet. If you need a different sheet:

```python
# Option A: Save specific sheet as CSV in Excel
# Option B: Create a simple script to handle multiple sheets
import pandas as pd
import lazyanalyst as la

# Read specific sheet
df = pd.read_excel("file.xlsx", sheet_name="Sheet2")
df.to_csv("temp.csv", index=False)

result = la.analyze("temp.csv")
```

### 2. Large Files

For very large files (>500MB), consider:

```python
import pandas as pd
import lazyanalyst as la

# Read only relevant columns
df = pd.read_csv("large_file.csv", usecols=['col1', 'col2', 'col3'])
df.to_csv("subset.csv", index=False)

result = la.analyze("subset.csv")
```

### 3. Filtering Data First

```python
import pandas as pd
import lazyanalyst as la

# Filter before analysis
df = pd.read_csv("sales.csv")
df_filtered = df[df['year'] == 2024]
df_filtered.to_csv("sales_2024.csv", index=False)

result = la.analyze("sales_2024.csv")
```

### 4. Batch Processing Multiple Files

```python
import lazyanalyst as la
import os

for filename in os.listdir("data/"):
    if filename.endswith(".csv"):
        print(f"Analyzing {filename}...")
        result = la.analyze(f"data/{filename}")
        print(f"✓ Complete: outputs/report.html")
```

### 5. Programmatic Access to Results

```python
import lazyanalyst as la

result = la.analyze("data.csv")

# Access different outputs
df_cleaned = result.cleaned_data()

# Compare original vs cleaned
print(f"Original shape: (?,?)")
print(f"Cleaned shape: {df_cleaned.shape}")

# Further analysis
print(df_cleaned.corr())
```

---

## Troubleshooting

### Issue: "FileNotFoundError"

**Cause:** File not found or path is incorrect

**Solution:**
```python
import os

# Check if file exists
filepath = "sales.csv"
if os.path.exists(filepath):
    result = la.analyze(filepath)
else:
    print(f"File not found: {filepath}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Available files: {os.listdir()}")
```

### Issue: "ValueError: Only supports .csv and .xlsx files"

**Cause:** File format not supported

**Solution:** Convert to CSV or Excel:
```python
import pandas as pd

# Convert from other format
df = pd.read_json("data.json")
df.to_csv("data.csv", index=False)

import lazyanalyst as la
result = la.analyze("data.csv")
```

### Issue: Dashboard/Report is blank

**Cause:** File path or outputs folder issue

**Solution:**
```python
import os

# Check outputs folder exists
if os.path.exists("outputs/dashboard.html"):
    print("File exists")
    print(f"File size: {os.path.getsize('outputs/dashboard.html')} bytes")
else:
    print("Run analyze again")
    
result = la.analyze("data.csv")
result.dashboard()
```

### Issue: Analysis is slow

**Cause:** Large file or many columns

**Solution:**
```python
# Option 1: Use fewer columns
import pandas as pd
df = pd.read_csv("large.csv", usecols=['col1', 'col2', 'col3'])
df.to_csv("small.csv", index=False)

# Option 2: Filter rows
df = df[df['year'] == 2024]  # Keep only recent data
df.to_csv("filtered.csv", index=False)

import lazyanalyst as la
result = la.analyze("filtered.csv")
```

---

## Next Steps

1. **Try it now** — Analyze your first dataset
2. **Explore outputs** — Open the dashboard and report
3. **Check insights** — See what LazyAnalyst discovered
4. **Read API docs** — See all available options
5. **Contribute** — Help improve LazyAnalyst!

---

## Documentation

- **API Reference** → `API_DOCUMENTATION.md`
- **Testing Guide** → `TESTING_GUIDE.md`
- **Main README** → `README.md`

---

## Questions or Issues?

- Check the FAQ in the main README
- Review the troubleshooting section above
- Open an issue on GitHub with details about your problem
- Include error messages and your Python version

Happy analyzing! 🎉
