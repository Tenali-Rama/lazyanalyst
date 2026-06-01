import pandas as pd
import numpy as np
import os

def clean(df, schema, quality_report):
    """cleans the dataset and returns cleaned df and actions list"""
    
    actions = []
    df_clean = df.copy()
    
    # make outputs folder if needed
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    # 1. Remove duplicate rows
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    after = len(df_clean)
    removed = before - after
    if removed > 0:
        actions.append(f"Removed {removed} duplicate rows")
        print(f"[LazyAnalyst] Removed {removed} duplicate rows")
    
    # 2. Fill missing values
    for col in df_clean.columns:
        missing_count = df_clean[col].isna().sum()
        if missing_count == 0:
            continue
        
        col_type = schema.get(col, 'categorical')
        
        # numerical -> median
        if col_type == 'numerical':
            median_val = df_clean[col].median()
            # FIXED: use assignment instead of inplace=True for pandas 3.x CoW
            df_clean[col] = df_clean[col].fillna(median_val)
            actions.append(f"Filled {missing_count} missing values in '{col}' with median ({median_val:.2f})")
            print(f"[LazyAnalyst] Filled {missing_count} missing in '{col}' with median")
        
        # categorical -> mode
        elif col_type == 'categorical':
            mode_val = df_clean[col].mode()
            if len(mode_val) > 0:
                mode_val = mode_val[0]
                # FIXED: use assignment instead of inplace=True
                df_clean[col] = df_clean[col].fillna(mode_val)
                actions.append(f"Filled {missing_count} missing values in '{col}' with mode ({mode_val})")
                print(f"[LazyAnalyst] Filled {missing_count} missing in '{col}' with mode")
            else:
                # fallback if no mode
                df_clean[col] = df_clean[col].fillna("unknown")
                actions.append(f"Filled {missing_count} missing values in '{col}' with 'unknown'")
        
        # datetime -> leave as-is (do nothing)
        elif col_type == 'datetime':
            actions.append(f"Left {missing_count} missing values in datetime column '{col}' as-is")
    
    # 3. Parse datetime columns
    for col in df_clean.columns:
        if schema.get(col) == 'datetime':
            try:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                actions.append(f"Parsed datetime column: '{col}'")
                print(f"[LazyAnalyst] Parsed datetime column: '{col}'")
            except Exception as e:
                actions.append(f"Warning: could not parse datetime column '{col}'")
                print(f"[LazyAnalyst] Warning: could not parse datetime column '{col}'")
    
    # 4. Flag outliers - FIXED: use is_numeric_dtype
    for col in df_clean.columns:
        if schema.get(col) == 'numerical' and pd.api.types.is_numeric_dtype(df_clean[col]):
            q1 = df_clean[col].quantile(0.25)
            q3 = df_clean[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outlier_flag = (df_clean[col] < lower) | (df_clean[col] > upper)
            col_name_outlier = f"{col}_is_outlier"
            df_clean[col_name_outlier] = outlier_flag
            outlier_count = outlier_flag.sum()
            if outlier_count > 0:
                actions.append(f"Flagged outliers in column: '{col}' ({outlier_count} rows)")
                print(f"[LazyAnalyst] Flagged outliers in column: '{col}' ({outlier_count} rows)")
    
    # save cleaned data
    df_clean.to_csv("outputs/cleaned_data.csv", index=False)
    print(f"[LazyAnalyst] Saved cleaned data to outputs/cleaned_data.csv")
    
    return df_clean, actions
