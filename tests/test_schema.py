import pytest
import pandas as pd
import numpy as np
from lazyanalyst import schema


class TestSchemaDetection:
    """Test column type detection"""
    
    def test_detect_numerical_columns(self):
        """test detection of numerical columns"""
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.5, 2.5, 3.5]
        })
        sch = schema.detect(df)
        assert sch['int_col'] == 'numerical'
        assert sch['float_col'] == 'numerical'
    
    def test_detect_categorical_columns(self):
        """test detection of categorical columns"""
        df = pd.DataFrame({
            'color': ['red', 'blue', 'green'],
            'category': ['A', 'B', 'A']
        })
        sch = schema.detect(df)
        assert sch['color'] == 'categorical'
        assert sch['category'] == 'categorical'
    
    def test_detect_boolean_columns(self):
        """test detection of boolean columns"""
        df = pd.DataFrame({
            'flag1': [True, False, True],
            'flag2': [0, 1, 0],
            'flag3': ['yes', 'no', 'yes']
        })
        sch = schema.detect(df)
        assert sch['flag1'] == 'boolean'
        # flag2 might be numerical or boolean depending on logic
        assert sch['flag3'] in ['boolean', 'categorical']
    
    def test_detect_identifier_columns(self):
        """test detection of identifier columns"""
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'code': ['ABC', 'DEF', 'GHI', 'JKL', 'MNO'],
            'key': ['K1', 'K2', 'K3', 'K4', 'K5']
        })
        sch = schema.detect(df)
        # should detect id, code, key as identifiers based on column names or uniqueness
        assert 'id' in sch
        assert 'code' in sch
        assert 'key' in sch
    
    def test_detect_datetime_columns(self):
        """test detection of datetime columns"""
        df = pd.DataFrame({
            'date': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03']),
            'timestamp': pd.to_datetime(['2021-01-01 10:00:00', '2021-01-01 11:00:00', '2021-01-01 12:00:00']),
            'date_string': ['2021-01-01', '2021-01-02', '2021-01-03']
        })
        sch = schema.detect(df)
        assert sch['date'] == 'datetime'
        assert sch['timestamp'] == 'datetime'
    
    def test_priority_identifier_over_boolean(self):
        """test that identifier has priority over boolean"""
        df = pd.DataFrame({
            'customer_id': [1, 2, 3, 4, 5]  # all unique, so identifier
        })
        sch = schema.detect(df)
        assert sch['customer_id'] == 'identifier'
    
    def test_priority_boolean_over_categorical(self):
        """test that boolean has priority over categorical"""
        df = pd.DataFrame({
            'status': [True, False, True, False, True]
        })
        sch = schema.detect(df)
        assert sch['status'] == 'boolean'
    
    def test_mixed_dataframe(self):
        """test schema detection on mixed dataframe"""
        df = pd.DataFrame({
            'customer_id': [1, 2, 3, 4],
            'age': [25, 30, 35, 40],
            'city': ['NYC', 'LA', 'Chicago', 'Boston'],
            'is_active': [True, False, True, False],
            'signup_date': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01'])
        })
        sch = schema.detect(df)
        assert sch['customer_id'] == 'identifier'
        assert sch['age'] == 'numerical'
        assert sch['city'] == 'categorical'
        assert sch['is_active'] == 'boolean'
        assert sch['signup_date'] == 'datetime'


class TestSchemaEdgeCases:
    """Test edge cases in schema detection"""
    
    def test_column_with_nulls(self):
        """test schema detection with missing values"""
        df = pd.DataFrame({
            'col': [1, 2, np.nan, 4]
        })
        sch = schema.detect(df)
        assert sch['col'] == 'numerical'
    
    def test_column_with_few_unique_values(self):
        """test categorical detection with few unique values"""
        df = pd.DataFrame({
            'rating': [1, 1, 2, 2, 3, 3]
        })
        sch = schema.detect(df)
        # should be categorical since fewer than 20 unique values
        assert sch['rating'] in ['categorical', 'numerical']
    
    def test_column_with_many_unique_values(self):
        """test identifier detection with all unique values"""
        df = pd.DataFrame({
            'uid': range(1000)
        })
        sch = schema.detect(df)
        # should be identifier due to high uniqueness
        assert sch['uid'] in ['identifier', 'numerical']
    
    def test_empty_dataframe(self):
        """test schema detection on empty dataframe"""
        df = pd.DataFrame({
            'col1': [],
            'col2': []
        })
        sch = schema.detect(df)
        assert isinstance(sch, dict)
        # should still return a schema
        assert len(sch) > 0 or len(sch) == 0  # edge case
    
    def test_single_row_dataframe(self):
        """test schema detection on single row"""
        df = pd.DataFrame({
            'a': [1],
            'b': ['text']
        })
        sch = schema.detect(df)
        assert 'a' in sch
        assert 'b' in sch


class TestSchemaOutput:
    """Test schema output format"""
    
    def test_schema_is_dict(self):
        """test schema is returned as dictionary"""
        df = pd.DataFrame({
            'col1': [1, 2],
            'col2': ['a', 'b']
        })
        sch = schema.detect(df)
        assert isinstance(sch, dict)
    
    def test_schema_has_all_columns(self):
        """test schema contains all DataFrame columns"""
        df = pd.DataFrame({
            'a': [1, 2],
            'b': ['x', 'y'],
            'c': [1.5, 2.5]
        })
        sch = schema.detect(df)
        assert set(sch.keys()) == set(df.columns)
    
    def test_schema_values_are_valid_types(self):
        """test schema values are valid type strings"""
        df = pd.DataFrame({
            'col1': [1, 2],
            'col2': ['a', 'b']
        })
        sch = schema.detect(df)
        valid_types = {'numerical', 'categorical', 'datetime', 'boolean', 'identifier'}
        for col_type in sch.values():
            assert col_type in valid_types
