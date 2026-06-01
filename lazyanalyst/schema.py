import pandas as pd
import numpy as np

def detect(df):
    """classifies each column into a type"""
    schema = {}
    
    # priority: identifier > boolean > datetime > categorical > numerical
    
    for col in df.columns:
        col_lower = col.lower()
        unique_vals = df[col].nunique()
        total_rows = len(df)
        
        # check for identifier first - FIXED: use word boundary matching
        is_identifier = False
        if unique_vals == total_rows:
            is_identifier = True
        else:
            # check for id/code/key with word boundaries
            for keyword in ['_id', 'id_', '_code', 'code_', '_key', 'key_']:
                if keyword in col_lower:
                    is_identifier = True
                    break
            # also check if column is exactly 'id'
            if col_lower == 'id':
                is_identifier = True
        
        if is_identifier:
            schema[col] = 'identifier'
            print(f"  {col} -> identifier")
            continue
        
        # check boolean
        if unique_vals == 2:
            # check if values are True/False, 0/1, yes/no
            unique_vals_set = set(df[col].dropna().astype(str).str.lower())
            if unique_vals_set.issubset({'true', 'false', '1', '0', 'yes', 'no'}):
                schema[col] = 'boolean'
                print(f"  {col} -> boolean")
                continue
        
        # check datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            schema[col] = 'datetime'
            print(f"  {col} -> datetime")
            continue
        
        # check column name for datetime keywords
        if any(word in col_lower for word in ['date', 'time', 'year', 'month', 'day', 'timestamp']):
            # try to convert
            try:
                pd.to_datetime(df[col])
                schema[col] = 'datetime'
                print(f"  {col} -> datetime")
                continue
            except:
                pass  # fall through to next type
        
        # check categorical
        if df[col].dtype == 'object' or unique_vals < 20:
            schema[col] = 'categorical'
            print(f"  {col} -> categorical")
            continue
        
        # default to numerical
        if pd.api.types.is_numeric_dtype(df[col]):
            schema[col] = 'numerical'
            print(f"  {col} -> numerical")
        else:
            # fallback for anything else
            schema[col] = 'categorical'
            print(f"  {col} -> categorical (fallback)")
    
    print(f"[LazyAnalyst] Schema detection complete: {len(schema)} columns classified")
    return schema
