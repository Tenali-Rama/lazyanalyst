import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate(df, schema):
    """generates and saves all charts"""
    
    # make plots folder
    if not os.path.exists("outputs/plots"):
        os.makedirs("outputs/plots")
    
    saved_files = []
    
    # get column types
    num_cols = [col for col in df.columns if schema.get(col) == 'numerical']
    cat_cols = [col for col in df.columns if schema.get(col) == 'categorical']
    date_cols = [col for col in df.columns if schema.get(col) == 'datetime']
    
    # 1. Correlation heatmap (if at least 2 numerical) - FIXED: use (10,6) instead of (10,8)
    if len(num_cols) >= 2:
        try:
            plt.figure(figsize=(10, 6))
            corr = df[num_cols].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plt.savefig('outputs/plots/heatmap.png', dpi=150)
            plt.close()
            saved_files.append('heatmap.png')
            print(f"[LazyAnalyst] Saved: outputs/plots/heatmap.png")
        except Exception as e:
            print(f"[LazyAnalyst] Warning: could not create heatmap - {e}")
    
    # 2. Missing values bar chart - FIXED: always generate the chart
    try:
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df)) * 100
        
        plt.figure(figsize=(10, 6))
        if missing_pct.sum() > 0:
            # plot only columns with missing data
            missing_pct[missing_pct > 0].sort_values(ascending=False).plot(kind='bar')
            plt.title('Missing Values by Column')
            plt.xlabel('Column')
            plt.ylabel('Missing Percentage (%)')
        else:
            # show all columns with 0 missing
            missing_pct.plot(kind='bar')
            plt.title('Missing Values by Column (No Missing Data)')
            plt.xlabel('Column')
            plt.ylabel('Missing Percentage (%)')
        
        plt.tight_layout()
        plt.savefig('outputs/plots/missing_values.png', dpi=150)
        plt.close()
        saved_files.append('missing_values.png')
        print(f"[LazyAnalyst] Saved: outputs/plots/missing_values.png")
    except Exception as e:
        print(f"[LazyAnalyst] Warning: missing values chart failed - {e}")
    
    # 3. Distribution plots for each numerical column
    for col in num_cols:
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[col].dropna(), kde=True, bins=30)
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.tight_layout()
            filename = f'outputs/plots/dist_{col}.png'
            plt.savefig(filename, dpi=150)
            plt.close()
            saved_files.append(f'dist_{col}.png')
            print(f"[LazyAnalyst] Saved: outputs/plots/dist_{col}.png")
        except Exception as e:
            print(f"[LazyAnalyst] Warning: could not plot distribution for {col} - {e}")
    
    # 4. Conditional charts (top 5 interesting pairs)
    # find interesting column pairs
    
    interesting_pairs = []
    
    # numerical vs numerical (use correlation strength)
    if len(num_cols) >= 2:
        corr_matrix = df[num_cols].corr().abs()
        # get top correlations
        pairs = []
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                pairs.append((num_cols[i], num_cols[j], corr_matrix.iloc[i, j]))
        pairs.sort(key=lambda x: x[2], reverse=True)
        # top 3 numerical-numerical
        for col1, col2, corr_val in pairs[:3]:
            interesting_pairs.append(('num_num', col1, col2))
    
    # categorical vs numerical (use mode? just take first few)
    if len(cat_cols) > 0 and len(num_cols) > 0:
        for i, cat in enumerate(cat_cols[:2]):  # limit to 2 categorical
            for j, num in enumerate(num_cols[:2]):  # limit to 2 numerical
                interesting_pairs.append(('cat_num', cat, num))
    
    # datetime vs numerical
    if len(date_cols) > 0 and len(num_cols) > 0:
        for date_col in date_cols[:1]:
            for num_col in num_cols[:3]:
                interesting_pairs.append(('date_num', date_col, num_col))
    
    # categorical vs categorical
    if len(cat_cols) >= 2:
        interesting_pairs.append(('cat_cat', cat_cols[0], cat_cols[1] if len(cat_cols)>1 else cat_cols[0]))
    
    # now generate charts for each pair type
    for pair_type, col1, col2 in interesting_pairs[:5]:  # limit to 5
        try:
            if pair_type == 'num_num':
                plt.figure(figsize=(10, 6))
                sns.scatterplot(data=df, x=col1, y=col2)
                plt.title(f'{col1} vs {col2}')
                filename = f'outputs/plots/scatter_{col1}_{col2}.png'
                plt.savefig(filename, dpi=150)
                plt.close()
                saved_files.append(f'scatter_{col1}_{col2}.png')
                print(f"[LazyAnalyst] Saved: {filename}")
            
            elif pair_type == 'cat_num':
                plt.figure(figsize=(10, 6))
                sns.boxplot(data=df, x=col1, y=col2)
                plt.title(f'{col2} by {col1}')
                plt.xticks(rotation=45)
                plt.tight_layout()
                filename = f'outputs/plots/box_{col1}_{col2}.png'
                plt.savefig(filename, dpi=150)
                plt.close()
                saved_files.append(f'box_{col1}_{col2}.png')
                print(f"[LazyAnalyst] Saved: {filename}")
            
            elif pair_type == 'date_num':
                # line plot over time
                plt.figure(figsize=(10, 6))
                # need to group by date? just plot as is
                temp = df[[col1, col2]].dropna().sort_values(col1)
                plt.plot(temp[col1], temp[col2], marker='o', linestyle='-', markersize=3)
                plt.title(f'{col2} over {col1}')
                plt.xlabel(col1)
                plt.ylabel(col2)
                plt.xticks(rotation=45)
                plt.tight_layout()
                filename = f'outputs/plots/line_{col1}_{col2}.png'
                plt.savefig(filename, dpi=150)
                plt.close()
                saved_files.append(f'line_{col1}_{col2}.png')
                print(f"[LazyAnalyst] Saved: {filename}")
            
            elif pair_type == 'cat_cat':
                plt.figure(figsize=(10, 6))
                # count plot
                count_data = df.groupby([col1, col2]).size().reset_index(name='count')
                # pivot for stacked bar? just use seaborn countplot
                sns.countplot(data=df, x=col1, hue=col2)
                plt.title(f'{col1} vs {col2}')
                plt.xticks(rotation=45)
                plt.tight_layout()
                filename = f'outputs/plots/count_{col1}_{col2}.png'
                plt.savefig(filename, dpi=150)
                plt.close()
                saved_files.append(f'count_{col1}_{col2}.png')
                print(f"[LazyAnalyst] Saved: {filename}")
                
        except Exception as e:
            print(f"[LazyAnalyst] Warning: could not create conditional plot for {col1},{col2} - {e}")
    
    print(f"[LazyAnalyst] Generated {len(saved_files)} chart files")
    return saved_files
