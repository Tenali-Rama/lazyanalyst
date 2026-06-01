import pandas as pd
import numpy as np
from scipy.stats import skew

def run(df, schema):
    """generates summary statistics and correlation matrix"""
    
    eda_results = {
        "numerical": {},
        "categorical": {},
        "correlation": {}
    }
    
    # get numerical columns
    num_cols = [col for col in df.columns if schema.get(col) == 'numerical']
    cat_cols = [col for col in df.columns if schema.get(col) == 'categorical']
    
    # 1. Numerical summary - FIXED: use is_numeric_dtype
    for col in num_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            data = df[col].dropna()
            if len(data) > 0:
                # using .iloc and .loc mix
                q1_val = data.quantile(0.25)
                q3_val = data.quantile(0.75)
                skewness = skew(data) if len(data) > 2 else 0
                
                eda_results["numerical"][col] = {
                    "mean": round(data.mean(), 4),
                    "median": round(data.median(), 4),
                    "std": round(data.std(), 4),
                    "variance": round(data.var(), 4),
                    "min": round(data.min(), 4),
                    "max": round(data.max(), 4),
                    "Q1": round(q1_val, 4),
                    "Q3": round(q3_val, 4),
                    "skewness": round(skewness, 4)
                }
    
    # 2. Categorical summary
    for col in cat_cols:
        if col in df.columns:
            data = df[col].dropna()
            if len(data) > 0:
                value_counts = data.value_counts()
                top5 = value_counts.head(5).to_dict()
                # convert top5 keys to string in case they are numbers
                top5_str = {str(k): v for k, v in top5.items()}
                
                eda_results["categorical"][col] = {
                    "unique": data.nunique(),
                    "top": top5_str
                }
    
    # 3. Correlation matrix (Pearson) for numerical columns
    if len(num_cols) >= 2:
        # make sure all exist and are numeric
        num_cols_exist = [c for c in num_cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
        if len(num_cols_exist) >= 2:
            corr_matrix = df[num_cols_exist].corr()
            # convert to nested dict
            corr_dict = {}
            for i in corr_matrix.index:
                corr_dict[i] = {}
                for j in corr_matrix.columns:
                    if i != j:
                        corr_dict[i][j] = round(corr_matrix.loc[i, j], 4)
            eda_results["correlation"] = corr_dict
    
    print(f"[LazyAnalyst] EDA complete: {len(num_cols)} numerical, {len(cat_cols)} categorical columns analyzed")
    
    return eda_results
