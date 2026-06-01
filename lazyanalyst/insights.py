import os

def generate(eda_results, stats_results, quality_report):
    """generates plain english insights from all results"""
    
    insights = []
    
    # 1. Correlation insights - FIXED: track seen pairs to avoid duplicates
    corr_data = eda_results.get("correlation", {})
    seen_pairs = set()
    for col1, related in corr_data.items():
        for col2, corr_val in related.items():
            # skip if we already processed the reverse pair
            pair = tuple(sorted([col1, col2]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            
            abs_corr = abs(corr_val)
            if abs_corr > 0.7:
                direction = "positive" if corr_val > 0 else "negative"
                insights.append(f"{col1} has a strong {direction} correlation with {col2}.")
            elif abs_corr > 0.4:
                direction = "positive" if corr_val > 0 else "negative"
                insights.append(f"{col1} has a moderate {direction} correlation with {col2}.")
    
    # 2. Group difference insights (from stats results)
    for stat in stats_results:
        if stat.get("significant", False):
            interp = stat.get("interpretation", "")
            if interp:
                insights.append(interp)
            # also extract group with highest mean if present
            # the interpretation already includes it
    
    # 3. Data quality insights
    missing_data = quality_report.get("missing", {})
    for col, info in missing_data.items():
        pct = info.get("pct", 0)
        if pct > 10:
            insights.append(f"{col} contains {pct}% missing values — consider reviewing this column.")
    
    dup_info = quality_report.get("duplicates", {})
    dup_count = dup_info.get("count", 0)
    if dup_count > 0:
        insights.append(f"The dataset contained {dup_count} duplicate rows, which were removed during cleaning.")
    
    # 4. Distribution insights (skewness from eda numerical summary)
    numerical_summary = eda_results.get("numerical", {})
    for col, stats_dict in numerical_summary.items():
        skew_val = stats_dict.get("skewness", 0)
        if skew_val > 2:
            insights.append(f"{col} is highly right-skewed. A log transform may be useful.")
        elif skew_val < -2:
            insights.append(f"{col} is highly left-skewed.")
    
    # remove duplicates from insights list (keep first occurrence)
    unique_insights = []
    for ins in insights:
        if ins not in unique_insights:
            unique_insights.append(ins)
    
    # save to file
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    with open("outputs/insights.txt", "w") as f:
        for ins in unique_insights:
            f.write(ins + "\n")
    
    print(f"[LazyAnalyst] Generated {len(unique_insights)} insights and saved to outputs/insights.txt")
    return unique_insights
