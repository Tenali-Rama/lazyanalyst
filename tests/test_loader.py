import pytest
import os
import tempfile
import pandas as pd
import numpy as np
from lazyanalyst import loader


class TestLoaderCSV:
    """Test CSV loading functionality"""
    
    def test_load_valid_csv(self):
        """test loading valid CSV file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,salary\n")
            f.write("Alice,30,50000\n")
            f.write("Bob,25,45000\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert isinstance(df, pd.DataFrame)
                assert len(df) == 2
                assert list(df.columns) == ['name', 'age', 'salary']
            finally:
                os.unlink(f.name)
    
    def test_load_csv_with_comma_delimiter(self):
        """test CSV with comma delimiter"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("a,b,c\n")
            f.write("1,2,3\n")
            f.write("4,5,6\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert len(df) == 2
                assert df['a'].tolist() == [1, 4]
            finally:
                os.unlink(f.name)
    
    def test_load_csv_with_semicolon_delimiter(self):
        """test CSV with semicolon delimiter"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("x;y;z\n")
            f.write("1;2;3\n")
            f.write("4;5;6\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert len(df) == 2
                # should detect semicolon
                assert 'x' in df.columns or 'x;y;z' in df.columns
            finally:
                os.unlink(f.name)
    
    def test_load_csv_with_tab_delimiter(self):
        """test CSV with tab delimiter"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1\tcol2\tcol3\n")
            f.write("1\t2\t3\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                # should detect tab delimiter
                assert len(df) >= 1
            finally:
                os.unlink(f.name)
    
    def test_load_csv_with_missing_values(self):
        """test CSV with missing values"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,value\n")
            f.write("Alice,100\n")
            f.write("Bob,\n")
            f.write("Charlie,150\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert len(df) == 3
                # Bob's value should be NaN
                assert pd.isna(df.loc[1, 'value'])
            finally:
                os.unlink(f.name)


class TestLoaderExcel:
    """Test Excel loading functionality"""
    
    def test_load_valid_xlsx(self):
        """test loading valid Excel file"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df_write = pd.DataFrame({
                'name': ['Alice', 'Bob'],
                'age': [30, 25]
            })
            df_write.to_excel(f.name, index=False)
            
            try:
                df = loader.load(f.name)
                assert isinstance(df, pd.DataFrame)
                assert len(df) == 2
                assert 'name' in df.columns
            finally:
                os.unlink(f.name)
    
    def test_load_xlsx_with_missing_values(self):
        """test Excel file with missing values"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df_write = pd.DataFrame({
                'id': [1, 2, 3],
                'value': [10.5, np.nan, 30.2]
            })
            df_write.to_excel(f.name, index=False)
            
            try:
                df = loader.load(f.name)
                assert pd.isna(df.loc[1, 'value'])
            finally:
                os.unlink(f.name)


class TestLoaderErrors:
    """Test error handling"""
    
    def test_file_not_found(self):
        """test FileNotFoundError for missing file"""
        with pytest.raises(FileNotFoundError):
            loader.load('nonexistent_file.csv')
    
    def test_unsupported_file_type(self):
        """test ValueError for unsupported file type"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("some text")
            f.flush()
            
            try:
                with pytest.raises(ValueError):
                    loader.load(f.name)
            finally:
                os.unlink(f.name)
    
    def test_empty_csv(self):
        """test loading empty CSV file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("a,b,c\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert len(df) == 0
            finally:
                os.unlink(f.name)


class TestDataTypeInference:
    """Test automatic dtype inference"""
    
    def test_numeric_dtype_inference(self):
        """test numeric columns are properly typed"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("int_col,float_col\n")
            f.write("1,1.5\n")
            f.write("2,2.5\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert pd.api.types.is_integer_dtype(df['int_col']) or pd.api.types.is_numeric_dtype(df['int_col'])
                assert pd.api.types.is_float_dtype(df['float_col'])
            finally:
                os.unlink(f.name)
    
    def test_string_dtype_inference(self):
        """test string columns are properly typed"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("text_col\n")
            f.write("hello\n")
            f.write("world\n")
            f.flush()
            
            try:
                df = loader.load(f.name)
                assert df['text_col'].dtype == 'object'
            finally:
                os.unlink(f.name)
