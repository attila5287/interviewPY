import os
import pandas as pd

def csvToDataframe(FILE_NAME='fire_county_data.csv', STATIC_FOLDER='INT_02_PYTHON_PANDAS_FIRE_DATA'):
    """ RETURNS PANDAS DATAFRAME, REQUIRES FILENAME WITH .CSV EXTENSION 
    ALSO STATIC_FOLDER IF ANY DEFAULT NONE """
    BASE_DIR = os.getcwd()
    PATH_COMPILED = os.path.join(BASE_DIR, STATIC_FOLDER, FILE_NAME)
    _df = pd.read_csv(PATH_COMPILED, encoding="iso-8859-1", low_memory=False)
    print(" ------------------------------- csvToDataframe ")
    print("--- a quick peek at dataframe: ")
    print(_df.head())
    print("--- columns  data types: ")
    print(_df.dtypes)
    return _df

def describeDataField(DESC_FILE_NAME = 'fire_data_description.csv', targetIndex_no=8):
    desc_fire_df = csvToDataframe(FILE_NAME='fire_data_description.csv', STATIC_FOLDER='INT_02_PYTHON_PANDAS_FIRE_DATA')
    dict_keys = desc_fire_df['Column Heading']
    dict_values = desc_fire_df['Value Description']
    _dict = dict(zip(dict_keys, dict_values))
    _listKeys = list(dict_keys)
    print()
    print("--- all field labels on dataset provided with interview-assignment: ")
    print(dict_keys)
    print()
    print("--- a brief description for target field for data visualization: ")
    _fieldName = _listKeys[targetIndex_no]
    print(str(_fieldName) + ": \t " + _dict[_fieldName])
    print()
    return None


    