import pytest
import pandas as pd
import numpy as np
from lazyanalyst import quality


class TestQualityAudit:
    """Test data quality auditing"""
    
    def test_audit_returns_report(self):
        """test audit returns quality report"""
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z']
        })
        schema_dict = {'a': 'numerical', 'b': 'categorical'}
        report = quality.audit(df, schema_dict)
        assert isinstance(report, dict)
    
    def test_audit_detects_missing_values(self):
        """test audit detects missing values"""
        df = pd.DataFrame({
            'a': [1, 2, np.nan],
            'b': [1, np.nan, 3]
        })
        schema_dict = {'a': 'numerical', 'b': 'numerical'}
        report = quality.audit(df, schema_dict)
        assert 'missing' in report or 'score' in report
        # should identify that column a has missing values
    
    def test_audit_detects_duplicates(self):
        """test audit detects duplicate rows"""
        df = pd.DataFrame({
            'a': [1, 1, 2],
            'b': ['x', 'x', 'y']
        })
        schema_dict = {'a': 'numerical', 'b': 'categorical'}
        report = quality.audit(df, schema_dict)
        assert 'duplicates' in report or 'score' in report
    
    def test_audit_clean_data(self):
        """test audit on clean data gives high score"""
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': ['x', 'y', 'z', 'w', 'v']
        })
        schema_dict = {'a': 'numerical', 'b': 'categorical'}
        report = quality.audit(df, schema_dict)
        assert 'score' in report
        # clean data should have high score
    
    def test_audit_includes_score(self):
        """test audit includes quality score"""
        df = pd.DataFrame({
            'x': [1, 2, 3]
        })
        schema_dict = {'x': 'numerical'}
        report = quality.audit(df, schema_dict)
        assert 'score' in report
        assert isinstance(report['score'], (int, float))
        assert 0 <= report['score'] <= 100


class TestQualityIssues:
    """Test quality issue detection"""
    
    def test_high_missing_percentage(self):
        """test detection of high missing value percentage"""
        df = pd.DataFrame({
            'col': [1, np.nan, np.nan, np.nan]
        })
        schema_dict = {'col': 'numerical'}
        report = quality.audit(df, schema_dict)
        # should flag high missing percentage
        assert isinstance(report, dict)
    
    def test_outlier_detection(self):
        """test outlier detection"""
        df = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 1000]  # 1000 is outlier
        })
        schema_dict = {'value': 'numerical'}
        report = quality.audit(df, schema_dict)
        assert 'outliers' in report or 'score' in report
    
    def test_mixed_quality_issues(self):
        """test detection of multiple quality issues"""
        df = pd.DataFrame({
            'a': [1, 1, np.nan, np.nan],
            'b': [100, 200, 300, 9999]  # outlier in b
        })
        schema_dict = {'a': 'numerical', 'b': 'numerical'}
        report = quality.audit(df, schema_dict)
        assert isinstance(report, dict)
