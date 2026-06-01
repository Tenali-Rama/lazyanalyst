import pandas as pd
import numpy as np
from scipy.stats import skew

def engineer(df, schema):
    """adds new features to the dataframe"""
    
    df_new = df.copy()
    features_created = []
    
    # 1. From datetime columns
    for col in df_new.columns:
        if schema.get(col) == 'datetime':
            try:
                # ensure it's datetime
                if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
                    df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
                
                # extract components
                df_new[f'{col}_year'] = df_new[col].dt.year
                df_new[f'{col}_month'] = df_new[col].dt.month
                df_new[f'{col}_day'] = df_new[col].dt.day
                df_new[f'{col}_quarter'] = df_new[col].dt.quarter
                df_new[f'{col}_weekday'] = df_new[col].dt.weekday
                df_new[f'{col}_is_weekend'] = (df_new[col].dt.weekday >= 5).astype(int)
                
                features_created.append(f"Created {col}_year")
                features_created.append(f"Created {col}_month")
                features_created.append(f"Created {col}_day")
                features_created.append(f"Created {col}_quarter")
                features_created.append(f"Created {col}_weekday")
                features_created.append(f"Created {col}_is_weekend")
                
                print(f"[LazyAnalyst] Added datetime features from '{col}'")
            except Exception as e:
                print(f"[LazyAnalyst] Warning: could not extract datetime features from {col} - {e}")
    
    # 2. From categorical columns (label encoding)
    for col in df_new.columns:
        if schema.get(col) == 'categorical':
            try:
                # use pd.factorize for label encoding
                encoded, _ = pd.factorize(df_new[col])
                df_new[f'{col}_encoded'] = encoded
                features_created.append(f"Created {col}_encoded")
                print(f"[LazyAnalyst] Label encoded '{col}'")
            except Exception as e:
                print(f"[LazyAnalyst] Warning: could not encode {col} - {e}")
    
    # 3. From numerical columns (log transform if skewed)
    for col in df_new.columns:
        if schema.get(col) == 'numerical':
            # check skewness
            data = df_new[col].dropna()
            if len(data) > 2:
                skew_val = skew(data)
                if abs(skew_val) > 1.0:
                    try:
                        # using np.log1p to handle zeros
                        df_new[f'{col}_log'] = np.log1p(df_new[col])
                        features_created.append(f"Created {col}_log")
                        print(f"[LazyAnalyst] Added log transform for '{col}' (skewness={skew_val:.2f})")
                    except Exception as e:
                        print(f"[LazyAnalyst] Warning: could not log transform {col} - {e}")
    
    print(f"[LazyAnalyst] Total new features created: {len(features_created)}")
    return df_new, features_created