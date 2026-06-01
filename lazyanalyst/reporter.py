import os
import pandas as pd
import numpy as np

def build(all_results):
    """generates polished HTML report with all results"""
    
    # unpack everything
    cleaned_df = all_results.get("cleaned_df")
    schema = all_results.get("schema")
    quality_report = all_results.get("quality_report")
    cleaning_actions = all_results.get("cleaning_actions", [])
    eda_results = all_results.get("eda_results")
    features_created = all_results.get("features_created", [])
    stats_results = all_results.get("stats_results")
    insights_list = all_results.get("insights")
    filename = all_results.get("filename", "dataset")
    
    if cleaned_df is None:
        print("[LazyAnalyst] Warning: no cleaned dataframe for report")
        return
    
    # get some numbers
    n_rows = len(cleaned_df)
    n_cols = len(cleaned_df.columns)
    quality_score = quality_report.get("score", 0) if quality_report else 0
    
    # top 3 insights (first 3)
    top_insights = insights_list[:3] if insights_list else ["No insights available"]
    
    # start building HTML
    html = []
    html.append("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>LazyAnalyst Report</title>
        <style>
            body {
                background-color: #0f1117;
                color: #e0e0e0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1, h2, h3 {
                color: #4fc3f7;
            }
            h1 {
                border-bottom: 2px solid #4fc3f7;
                padding-bottom: 10px;
            }
            .section {
                margin-bottom: 40px;
                background: #1a1c23;
                padding: 20px;
                border-radius: 8px;
            }
            .score-box {
                font-size: 48px;
                font-weight: bold;
                color: #4fc3f7;
                text-align: center;
                padding: 20px;
                background: #2a2c35;
                border-radius: 8px;
                display: inline-block;
                margin: 10px 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th, td {
                text-align: left;
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            th {
                background-color: #2a2c35;
                color: #4fc3f7;
            }
            .two-column {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }
            .two-column > div {
                flex: 1;
                min-width: 250px;
            }
            .insight-list {
                list-style-type: none;
                padding-left: 0;
            }
            .insight-list li {
                background: #2a2c35;
                margin: 10px 0;
                padding: 12px;
                border-radius: 6px;
                border-left: 4px solid #4fc3f7;
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 4px;
                margin: 10px 0;
            }
            @media print {
                body {
                    background-color: white;
                    color: black;
                }
                .section {
                    background: white;
                    border: 1px solid #ccc;
                    page-break-inside: avoid;
                }
                h1, h2, h3 {
                    color: black;
                }
                .score-box {
                    color: black;
                    border: 1px solid black;
                }
                table {
                    border: 1px solid black;
                }
                th {
                    background-color: #eee;
                    color: black;
                }
                img {
                    max-width: 80%;
                }
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>LazyAnalyst Automated Report</h1>
    """)
    
    # 1. Executive Summary
    summary_text = f"The dataset '{filename}' contains {n_rows} rows and {n_cols} columns. " \
                   f"Data quality score is {quality_score}/100. " \
                   f"Top insights: {'. '.join(top_insights[:3])}"
    
    html.append(f"""
        <div class="section">
            <h2>Executive Summary</h2>
            <p>{summary_text}</p>
        </div>
    """)
    
    # 2. Dataset Overview
    html.append('<div class="section"><h2>Dataset Overview</h2>')
    html.append("""
        <table>
            <tr><th>Column</th><th>Type</th><th>Missing Count</th></tr>
    """)
    if schema:
        missing_info = quality_report.get("missing", {}) if quality_report else {}
        for col, col_type in schema.items():
            missing_count = missing_info.get(col, {}).get("count", 0)
            html.append(f"<tr><td>{col}</td><td>{col_type}</td><td>{missing_count}</td></tr>")
    html.append("</table></div>")
    
    # 3. Data Quality
    html.append('<div class="section"><h2>Data Quality</h2>')
    html.append(f'<div class="score-box">Quality Score: {quality_score}/100</div>')
    html.append("<h3>Issues Found</h3><ul>")
    if quality_report:
        missing_data = quality_report.get("missing", {})
        for col, info in missing_data.items():
            html.append(f"<li>{col}: {info['pct']}% missing ({info['count']} rows)</li>")
        dup_info = quality_report.get("duplicates", {})
        if dup_info.get("count", 0) > 0:
            html.append(f"<li>{dup_info['count']} duplicate rows ({dup_info['pct']}%)</li>")
        invalid_list = quality_report.get("invalid", [])
        for inv in invalid_list:
            html.append(f"<li>{inv}</li>")
        outliers_info = quality_report.get("outliers", {})
        for col, info in outliers_info.items():
            html.append(f"<li>{col}: {info['count']} outliers flagged</li>")
    else:
        html.append("<li>No quality report available</li>")
    html.append("</ul></div>")
    
    # 4. Cleaning Actions
    html.append('<div class="section"><h2>Cleaning Actions</h2><ul>')
    if cleaning_actions:
        for action in cleaning_actions:
            html.append(f"<li>{action}</li>")
    else:
        html.append("<li>No cleaning actions recorded</li>")
    html.append("</ul></div>")
    
    # 5. Exploratory Data Analysis
    html.append('<div class="section"><h2>Exploratory Data Analysis</h2>')
    
    # numerical summary table
    numerical_summary = eda_results.get("numerical", {}) if eda_results else {}
    if numerical_summary:
        html.append('<h3>Numerical Summary</h3><div class="two-column">')
        for col, stats_dict in numerical_summary.items():
            html.append(f"""
                <div>
                    <strong>{col}</strong><br>
                    Mean: {stats_dict.get('mean', 'N/A')}<br>
                    Median: {stats_dict.get('median', 'N/A')}<br>
                    Std: {stats_dict.get('std', 'N/A')}<br>
                    Min: {stats_dict.get('min', 'N/A')}<br>
                    Max: {stats_dict.get('max', 'N/A')}
                </div>
            """)
        html.append('</div>')
    
    # categorical summary
    categorical_summary = eda_results.get("categorical", {}) if eda_results else {}
    if categorical_summary:
        html.append('<h3>Categorical Summary</h3><div class="two-column">')
        for col, cat_dict in categorical_summary.items():
            top_items = cat_dict.get("top", {})
            top_str = ", ".join([f"{k}: {v}" for k, v in list(top_items.items())[:3]])
            html.append(f"""
                <div>
                    <strong>{col}</strong><br>
                    Unique values: {cat_dict.get('unique', 'N/A')}<br>
                    Top categories: {top_str}
                </div>
            """)
        html.append('</div>')
    html.append('</div>')
    
    # 6. Visualizations (embed all PNGs from plots folder)
    html.append('<div class="section"><h2>Visualizations</h2>')
    plots_dir = "outputs/plots"
    if os.path.exists(plots_dir):
        png_files = [f for f in os.listdir(plots_dir) if f.endswith('.png')]
        if png_files:
            for png in sorted(png_files):
                html.append(f'<img src="plots/{png}" alt="{png}"><br>')
        else:
            html.append("<p>No plots generated.</p>")
    else:
        html.append("<p>No plots folder found.</p>")
    html.append('</div>')
    
    # 7. Statistical Results
    html.append('<div class="section"><h2>Statistical Results</h2>')
    if stats_results:
        html.append("""
            <table>
                <tr><th>Test</th><th>Columns</th><th>Statistic</th><th>p-value</th><th>Significant</th><th>Interpretation</th></tr>
        """)
        for stat in stats_results:
            test = stat.get("test", "")
            cols = ", ".join(stat.get("columns", []))
            stat_val = stat.get("statistic", "N/A")
            p_val = stat.get("p_value", "N/A")
            sig = "Yes" if stat.get("significant", False) else "No"
            interp = stat.get("interpretation", "")
            html.append(f"<tr><td>{test}</td><td>{cols}</td><td>{stat_val}</td><td>{p_val}</td><td>{sig}</td><td>{interp}</td></tr>")
        html.append("</table>")
    else:
        html.append("<p>No statistical tests were run.</p>")
    html.append('</div>')
    
    # 8. Feature Engineering
    html.append('<div class="section"><h2>Feature Engineering</h2><ul>')
    if features_created:
        for feat in features_created:
            html.append(f"<li>{feat}</li>")
    else:
        html.append("<li>No features were created.</li>")
    html.append("</ul></div>")
    
    # 9. Insights
    html.append('<div class="section"><h2>Insights</h2><ol class="insight-list">')
    if insights_list:
        for ins in insights_list:
            html.append(f"<li>{ins}</li>")
    else:
        html.append("<li>No insights generated.</li>")
    html.append("</ol></div>")
    
    html.append("</div></body></html>")
    
    # save the report
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/report.html", "w", encoding="utf-8") as f:
        f.write("".join(html))
    print("[LazyAnalyst] Report saved to outputs/report.html")