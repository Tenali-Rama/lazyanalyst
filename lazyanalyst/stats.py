import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr, f_oneway, chi2_contingency, ttest_ind

def run(df, schema):
    """runs statistical tests on interesting column pairs"""
    
    results = []
    
    # get column types
    num_cols = [col for col in df.columns if schema.get(col) == 'numerical']
    cat_cols = [col for col in df.columns if schema.get(col) == 'categorical']
    
    # helper to check skewness (roughly normal if skew < 1)
    def is_normalish(col):
        data = df[col].dropna()
        if len(data) < 3:
            return True
        skew_val = abs(data.skew())
        return skew_val < 1.0
    
    # 1. Numerical vs Numerical (Pearson or Spearman)
    if len(num_cols) >= 2:
        pairs = []
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                col1, col2 = num_cols[i], num_cols[j]
                # check if both exist and have enough data
                temp = df[[col1, col2]].dropna()
                if len(temp) >= 3:
                    # decide test
                    if is_normalish(col1) and is_normalish(col2):
                        test_name = "Pearson Correlation"
                        corr, p_val = pearsonr(temp[col1], temp[col2])
                    else:
                        test_name = "Spearman Correlation"
                        corr, p_val = spearmanr(temp[col1], temp[col2])
                    
                    significant = p_val < 0.05
                    # interpretation
                    abs_corr = abs(corr)
                    if abs_corr > 0.7:
                        direction = "strong positive" if corr > 0 else "strong negative"
                        interp = f"{col1} and {col2} have a {direction} relationship."
                    elif abs_corr > 0.4:
                        direction = "moderate positive" if corr > 0 else "moderate negative"
                        interp = f"{col1} and {col2} have a {direction} relationship."
                    else:
                        interp = f"{col1} and {col2} have a weak relationship."
                    
                    results.append({
                        "test": test_name,
                        "columns": [col1, col2],
                        "statistic": round(corr, 4),
                        "p_value": round(p_val, 6),
                        "significant": significant,
                        "interpretation": interp
                    })
                    print(f"[LazyAnalyst] {test_name}: {col1} vs {col2} = {corr:.3f} (p={p_val:.4f})")
    
    # 2. Categorical vs Numerical (t-test or ANOVA)
    for cat_col in cat_cols:
        for num_col in num_cols:
            # drop missing in both
            temp = df[[cat_col, num_col]].dropna()
            if len(temp) == 0:
                continue
            
            groups = temp.groupby(cat_col)[num_col].apply(list)
            unique_cats = len(groups)
            
            if unique_cats == 2:
                # Independent T-Test
                group_vals = list(groups)
                if len(group_vals[0]) > 0 and len(group_vals[1]) > 0:
                    t_stat, p_val = ttest_ind(group_vals[0], group_vals[1])
                    test_name = "Independent T-Test"
                    significant = p_val < 0.05
                    
                    # find which group has higher mean
                    means = {cat: np.mean(groups[cat]) for cat in groups.index}
                    highest_cat = max(means, key=means.get)
                    interp = f"{cat_col} has a statistically significant effect on {num_col}." if significant else f"No significant difference in {num_col} between {cat_col} groups."
                    if significant:
                        interp += f" Group '{highest_cat}' has the highest average {num_col}."
                    
                    results.append({
                        "test": test_name,
                        "columns": [cat_col, num_col],
                        "statistic": round(t_stat, 4),
                        "p_value": round(p_val, 6),
                        "significant": significant,
                        "interpretation": interp
                    })
                    print(f"[LazyAnalyst] T-Test: {cat_col} ({unique_cats} groups) vs {num_col} (p={p_val:.4f})")
            
            elif unique_cats >= 3:
                # ANOVA
                group_vals = [grp for grp in groups if len(grp) > 0]
                if len(group_vals) >= 3:
                    f_stat, p_val = f_oneway(*group_vals)
                    test_name = "ANOVA"
                    significant = p_val < 0.05
                    
                    # find highest mean group
                    means = {cat: np.mean(groups[cat]) for cat in groups.index}
                    highest_cat = max(means, key=means.get)
                    interp = f"{cat_col} has a statistically significant effect on {num_col}." if significant else f"No significant difference in {num_col} across {cat_col} categories."
                    if significant:
                        interp += f" Category '{highest_cat}' has the highest average {num_col}."
                    
                    results.append({
                        "test": test_name,
                        "columns": [cat_col, num_col],
                        "statistic": round(f_stat, 4),
                        "p_value": round(p_val, 6),
                        "significant": significant,
                        "interpretation": interp
                    })
                    print(f"[LazyAnalyst] ANOVA: {cat_col} vs {num_col} (p={p_val:.4f})")
    
    # 3. Categorical vs Categorical (Chi-Square)
    if len(cat_cols) >= 2:
        # limit to top 5 pairs to avoid explosion
        for i in range(len(cat_cols)):
            for j in range(i+1, len(cat_cols)):
                if len(results) > 20:  # keep total under limit
                    break
                col1, col2 = cat_cols[i], cat_cols[j]
                # create contingency table
                contingency = pd.crosstab(df[col1], df[col2])
                if contingency.shape[0] > 1 and contingency.shape[1] > 1:
                    chi2, p_val, dof, expected = chi2_contingency(contingency)
                    significant = p_val < 0.05
                    interp = f"There is a significant association between {col1} and {col2}." if significant else f"No significant association between {col1} and {col2}."
                    results.append({
                        "test": "Chi-Square Test",
                        "columns": [col1, col2],
                        "statistic": round(chi2, 4),
                        "p_value": round(p_val, 6),
                        "significant": significant,
                        "interpretation": interp
                    })
                    print(f"[LazyAnalyst] Chi-Square: {col1} vs {col2} (p={p_val:.4f})")
    
    # limit to 10 most relevant (just take first 10)
    final_results = results[:10]
    print(f"[LazyAnalyst] Statistical tests completed: {len(final_results)} results")
    return final_results