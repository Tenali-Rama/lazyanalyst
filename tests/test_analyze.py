import pytest
import os
import tempfile
import pandas as pd
import shutil
from lazyanalyst import analyze


class TestAnalyzePipeline:
    """Test the main analyze pipeline"""
    
    def setup_method(self):
        """setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        
        # create a simple CSV file for testing
        self.test_csv = os.path.join(self.temp_dir, 'test_data.csv')
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 75000, 80000, 95000],
            'department': ['Sales', 'IT', 'HR', 'Sales', 'IT'],
            'is_manager': [False, True, False, True, False]
        })
        df.to_csv(self.test_csv, index=False)
    
    def teardown_method(self):
        """cleanup after tests"""
        if os.path.exists('outputs'):
            shutil.rmtree('outputs')
        os.chdir('..')
        shutil.rmtree(self.temp_dir)
    
    def test_analyze_returns_result_object(self):
        """test analyze returns LazyAnalystResult"""
        result = analyze.analyze(self.test_csv)
        assert result is not None
        assert hasattr(result, 'report')
        assert hasattr(result, 'dashboard')
        assert hasattr(result, 'cleaned_data')
    
    def test_analyze_creates_outputs_folder(self):
        """test analyze creates outputs folder"""
        analyze.analyze(self.test_csv)
        assert os.path.exists('outputs')
        assert os.path.isdir('outputs')
    
    def test_analyze_creates_report_html(self):
        """test analyze creates report.html"""
        analyze.analyze(self.test_csv, report=True, dashboard=False)
        assert os.path.exists('outputs/report.html')
    
    def test_analyze_creates_dashboard_html(self):
        """test analyze creates dashboard.html"""
        analyze.analyze(self.test_csv, report=False, dashboard=True)
        assert os.path.exists('outputs/dashboard.html')
    
    def test_analyze_skips_report_when_disabled(self):
        """test analyze skips report when report=False"""
        result = analyze.analyze(self.test_csv, report=False, dashboard=False)
        assert result is not None
        # report should not be created
        assert result.report_path == "" or result.report_path is None
    
    def test_analyze_cleaned_data_accessible(self):
        """test cleaned data is accessible from result"""
        result = analyze.analyze(self.test_csv)
        cleaned_df = result.cleaned_data()
        assert isinstance(cleaned_df, pd.DataFrame)
        assert len(cleaned_df) > 0
    
    def test_analyze_with_missing_values(self):
        """test analyze handles data with missing values"""
        csv_with_nulls = os.path.join(self.temp_dir, 'test_nulls.csv')
        df = pd.DataFrame({
            'value': [1, 2, None, 4],
            'name': ['A', None, 'C', 'D']
        })
        df.to_csv(csv_with_nulls, index=False)
        
        result = analyze.analyze(csv_with_nulls)
        assert result is not None
        cleaned = result.cleaned_data()
        assert isinstance(cleaned, pd.DataFrame)
    
    def test_analyze_with_duplicates(self):
        """test analyze handles duplicate rows"""
        csv_with_dupes = os.path.join(self.temp_dir, 'test_dupes.csv')
        df = pd.DataFrame({
            'id': [1, 1, 2, 3],
            'value': [10, 10, 20, 30]
        })
        df.to_csv(csv_with_dupes, index=False)
        
        result = analyze.analyze(csv_with_dupes)
        assert result is not None


class TestAnalyzeErrorHandling:
    """Test error handling in analyze"""
    
    def setup_method(self):
        """setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """cleanup after tests"""
        if os.path.exists('outputs'):
            shutil.rmtree('outputs')
        os.chdir('..')
        shutil.rmtree(self.temp_dir)
    
    def test_analyze_nonexistent_file(self):
        """test analyze with nonexistent file"""
        result = analyze.analyze('nonexistent.csv')
        assert result is None
    
    def test_analyze_invalid_file_type(self):
        """test analyze with invalid file type"""
        invalid_file = os.path.join(self.temp_dir, 'test.txt')
        with open(invalid_file, 'w') as f:
            f.write("invalid content")
        
        result = analyze.analyze(invalid_file)
        assert result is None


class TestAnalyzeResultObject:
    """Test the LazyAnalystResult class"""
    
    def setup_method(self):
        """setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        
        # create test data
        self.test_csv = os.path.join(self.temp_dir, 'test.csv')
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6]
        })
        df.to_csv(self.test_csv, index=False)
    
    def teardown_method(self):
        """cleanup after tests"""
        if os.path.exists('outputs'):
            shutil.rmtree('outputs')
        os.chdir('..')
        shutil.rmtree(self.temp_dir)
    
    def test_result_cleaned_data_returns_dataframe(self):
        """test result.cleaned_data() returns DataFrame"""
        result = analyze.analyze(self.test_csv)
        cleaned = result.cleaned_data()
        assert isinstance(cleaned, pd.DataFrame)
    
    def test_result_has_paths(self):
        """test result object has file paths"""
        result = analyze.analyze(self.test_csv, report=True, dashboard=True)
        assert result.cleaned_data_path is not None
        assert result.report_path is not None or result.report_path == ""
        assert result.dashboard_path is not None or result.dashboard_path == ""
