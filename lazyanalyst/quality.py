import pandas as pd
import numpy as np
from datetime import datetime

def audit(df, schema):
    """produces quality report dictionary"""
    
    quality_report = {}
    
    # 1. missing values
    missing_data = {}
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        if missing_count > 0:
            missing_data[col] = {"count": missing_count, "pct": round(missing_pct, 2)}
            # flag high missing (>20%)
            if missing_pct > 20:
                print(f"[LazyAnalyst] Column '{col}' has high missing: {missing_pct:.1f}%")
    
    quality_report["missing"] = missing_data
    
    # 2. duplicate rows
    dup_count = df.duplicated().sum()
    dup_pct = (dup_count / len(df)) * 100 if len(df) > 0 else 0
    quality_report["duplicates"] = {"count": dup_count, "pct": round(dup_pct, 2)}
    if dup_count > 0:
        print(f"[LazyAnalyst] Found {dup_count} duplicate rows ({dup_pct:.1f}%)")
    
    # 3. outliers for numerical columns - FIXED: use is_numeric_dtype
    outliers_dict = {}
    for col in df.columns:
        if schema.get(col) == 'numerical' and pd.api.types.is_numeric_dtype(df[col]):
            # IQR method
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            if outlier_count > 0:
                outliers_dict[col] = {"count": int(outlier_count)}
                print(f"[LazyAnalyst] Column '{col}' has {outlier_count} outliers")
    
    quality_report["outliers"] = outliers_dict
    
    # 4. invalid data
    invalid_list = []
    
    # negative values in certain columns
    negative_keywords = ['age', 'price', 'quantity', 'count', 'amount', 'salary']
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in negative_keywords):
            if pd.api.types.is_numeric_dtype(df[col]):
                neg_count = (df[col] < 0).sum()
                if neg_count > 0:
                    invalid_list.append(f"negative values in '{col}' column ({neg_count} rows)")
                    print(f"[LazyAnalyst] Invalid: negative values in '{col}'")
    
    # future dates in datetime columns
    today = datetime.now().date()
    for col in df.columns:
        if schema.get(col) == 'datetime':
            try:
                # try to convert to datetime if not already
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    temp_dates = pd.to_datetime(df[col], errors='coerce')
                else:
                    temp_dates = df[col]
                future_mask = temp_dates.dt.date > today
                future_count = future_mask.sum()
                if future_count > 0:
                    invalid_list.append(f"future dates in '{col}' column ({future_count} rows)")
                    print(f"[LazyAnalyst] Invalid: future dates in '{col}'")
            except:
                pass  # skip if conversion fails
    
    quality_report["invalid"] = invalid_list
    
    # Data Quality Score
    score = 100
    
    # subtract for high missing
    for col, info in missing_data.items():
        if info["pct"] > 20:
            score -= 10
        elif info["pct"] > 5:
            score -= 5
    
    # subtract for duplicates > 1%
    if dup_pct > 1:
        score -= 5
    
    # subtract for outliers > 5% of values
    for col, info in outliers_dict.items():
        outlier_pct = (info["count"] / len(df)) * 100
        if outlier_pct > 5:
            score -= 2
    
    # floor at 0
    if score < 0:
        score = 0
    
    quality_report["score"] = score
    
    print(f"[LazyAnalyst] Data Quality Score: {score}/100")
    
    return quality_report
