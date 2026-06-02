import pandas as pd
import numpy as np
import os

def load(filepath):
    """loads csv or excel file into dataframe"""
    
    # check if file exists before trying to read
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"LazyAnalyst could not find the file: {filepath}")
    
    # check file type
    if not (filepath.endswith('.csv') or filepath.endswith('.xlsx')):
        raise ValueError("LazyAnalyst only supports .csv and .xlsx files.")
    
    try:
        if filepath.endswith('.csv'):
            # try different delimiters
            df = None
            for delim in [',', ';', '\t']:
                try:
                    df = pd.read_csv(filepath, delimiter=delim, encoding='utf-8', encoding_errors='replace')
                    if df.shape[1] > 1:  # if more than one column, probably correct delimiter
                        break
                except:
                    continue
            
            if df is None or df.empty:
                # fallback - try without delimiter
                df = pd.read_csv(filepath, encoding='utf-8', encoding_errors='replace')
            
            print(f"[LazyAnalyst] Loaded CSV: {filepath}")
            
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
            print(f"[LazyAnalyst] Loaded Excel: {filepath}")
        
        # infer dtypes conservatively - keep object dtype for strings
        df = df.infer_objects()
        
        # print shape
        print(f"[LazyAnalyst] Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        return df
    
    except Exception as e:
        print(f"[LazyAnalyst] Warning: loader failed — {e}. Skipping this step.")
        return pd.DataFrame()
