import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

def build(all_results):
    """builds and saves self-contained dashboard HTML"""
    
    # unpack results (this is messy but works)
    cleaned_df = all_results.get("cleaned_df")
    schema = all_results.get("schema")
    quality_report = all_results.get("quality_report")
    eda_results = all_results.get("eda_results")
    stats_results = all_results.get("stats_results")
    insights_list = all_results.get("insights")
    
    if cleaned_df is None:
        print("[LazyAnalyst] Warning: no cleaned dataframe for dashboard")
        return
    
    # get dataset info
    filename = all_results.get("filename", "dataset")
    n_rows = len(cleaned_df)
    n_cols = len(cleaned_df.columns)
    quality_score = quality_report.get("score", 0) if quality_report else 0
    
    # start building HTML
    html_parts = []
    html_parts.append("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>LazyAnalyst Dashboard</title>
        <style>
            body {
                background-color: #0f1117;
                color: #e0e0e0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
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
            .metric {
                display: inline-block;
                background: #2a2c35;
                padding: 10px 20px;
                border-radius: 6px;
                margin-right: 15px;
                margin-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th, td {
                text-align: left;
                padding: 10px;
                border-bottom: 1px solid #333;
            }
            th {
                background-color: #2a2c35;
                color: #4fc3f7;
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
            .chart-container {
                margin: 20px 0;
                padding: 10px;
                background: #1a1c23;
                border-radius: 6px;
            }
            .two-column {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }
            .two-column > div {
                flex: 1;
                min-width: 300px;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>LazyAnalyst Dashboard</h1>
    """)
    
    # 1. Overview section
    html_parts.append(f"""
        <div class="section">
            <h2>Overview</h2>
            <div class="metric">📄 Dataset: {filename}</div>
            <div class="metric">📊 Rows: {n_rows}</div>
            <div class="metric">📋 Columns: {n_cols}</div>
            <div class="metric">⭐ Quality Score: {quality_score}/100</div>
            <h3>Columns & Types</h3>
            <table>
                <tr><th>Column Name</th><th>Detected Type</th></tr>
    """)
    
    if schema:
        for col, col_type in schema.items():
            html_parts.append(f"<tr><td>{col}</td><td>{col_type}</td></tr>")
    html_parts.append("</table></div>")
    
    # 2. Data Quality section
    missing_data = quality_report.get("missing", {}) if quality_report else {}
    dup_info = quality_report.get("duplicates", {"count":0, "pct":0}) if quality_report else {"count":0, "pct":0}
    outliers_info = quality_report.get("outliers", {}) if quality_report else {}
    
    # missing values bar chart (plotly)
    if missing_data:
        missing_cols = list(missing_data.keys())
        missing_pcts = [missing_data[c]["pct"] for c in missing_cols]
        fig_missing = px.bar(x=missing_cols, y=missing_pcts, labels={'x':'Column', 'y':'Missing (%)'}, title="Missing Values by Column")
        fig_missing.update_layout(template="plotly_dark", paper_bgcolor="#1a1c23", plot_bgcolor="#1a1c23")
        html_parts.append(f"""
        <div class="section">
            <h2>Data Quality</h2>
            <div class="chart-container">
                {fig_missing.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <p>Duplicate rows: {dup_info['count']} ({dup_info['pct']}%)</p>
            <p>Outliers flagged in columns: {', '.join(outliers_info.keys()) if outliers_info else 'none'}</p>
        </div>
        """)
    else:
        html_parts.append(f"""
        <div class="section">
            <h2>Data Quality</h2>
            <p>No missing values found.</p>
            <p>Duplicate rows: {dup_info['count']} ({dup_info['pct']}%)</p>
            <p>Outliers flagged in columns: {', '.join(outliers_info.keys()) if outliers_info else 'none'}</p>
        </div>
        """)
    
    # 3. Distributions
    num_cols = [col for col in schema if schema[col]=='numerical'] if schema else []
    cat_cols = [col for col in schema if schema[col]=='categorical'] if schema else []
    
    html_parts.append('<div class="section"><h2>Distributions</h2>')
    # histograms for numerical
    for col in num_cols[:5]:  # limit to 5
        fig_hist = px.histogram(cleaned_df, x=col, nbins=30, title=f"Distribution of {col}", template="plotly_dark")
        fig_hist.update_layout(paper_bgcolor="#1a1c23", plot_bgcolor="#1a1c23")
        html_parts.append(f'<div class="chart-container">{fig_hist.to_html(full_html=False, include_plotlyjs="cdn")}</div>')
    
    # bar charts for categorical (top 10)
    for col in cat_cols[:5]:
        top10 = cleaned_df[col].value_counts().nlargest(10).reset_index()
        top10.columns = [col, 'count']
        fig_bar = px.bar(top10, x=col, y='count', title=f"Top 10 categories in {col}", template="plotly_dark")
        fig_bar.update_layout(paper_bgcolor="#1a1c23", plot_bgcolor="#1a1c23")
        html_parts.append(f'<div class="chart-container">{fig_bar.to_html(full_html=False, include_plotlyjs="cdn")}</div>')
    html_parts.append('</div>')
    
    # 4. Correlations (heatmap)
    if len(num_cols) >= 2:
        corr_matrix = cleaned_df[num_cols].corr()
        fig_corr = go.Figure(data=go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns, colorscale='RdBu', zmid=0))
        fig_corr.update_layout(title="Correlation Heatmap", template="plotly_dark", paper_bgcolor="#1a1c23", plot_bgcolor="#1a1c23")
        html_parts.append(f"""
        <div class="section">
            <h2>Correlations</h2>
            <div class="chart-container">{fig_corr.to_html(full_html=False, include_plotlyjs='cdn')}</div>
        </div>
        """)
    
    # 5. Statistical Tests (table)
    html_parts.append('<div class="section"><h2>Statistical Tests</h2>')
    if stats_results:
        html_parts.append("""
        <table>
            <tr><th>Test</th><th>Columns</th><th>p-value</th><th>Significant</th><th>Interpretation</th></tr>
        """)
        for stat in stats_results:
            test = stat.get("test", "")
            cols = ", ".join(stat.get("columns", []))
            p_val = stat.get("p_value", 1)
            sig = "Yes" if stat.get("significant", False) else "No"
            interp = stat.get("interpretation", "")
            html_parts.append(f"<tr><td>{test}</td><td>{cols}</td><td>{p_val}</td><td>{sig}</td><td>{interp}</td></tr>")
        html_parts.append("</table>")
    else:
        html_parts.append("<p>No statistical tests were run.</p>")
    html_parts.append('</div>')
    
    # 6. Insights
    html_parts.append('<div class="section"><h2>Insights</h2><ul class="insight-list">')
    if insights_list:
        for ins in insights_list:
            html_parts.append(f"<li>{ins}</li>")
    else:
        html_parts.append("<li>No insights generated.</li>")
    html_parts.append("</ul></div>")
    
    html_parts.append("</div></body></html>")
    
    # write to file
    full_html = "".join(html_parts)
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/dashboard.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("[LazyAnalyst] Dashboard saved to outputs/dashboard.html")