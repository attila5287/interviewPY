import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


def csvToDataframe(FILE_NAME='fire_county_data.csv', STATIC_FOLDER='INT_02_PYTHON_PANDAS_FIRE_DATA'):
    """ RETURNS PANDAS DATAFRAME, REQUIRES FILENAME WITH .CSV EXTENSION 
    ALSO STATIC_FOLDER IF ANY DEFAULT NONE """
    BASE_DIR = os.getcwd()
    PATH_COMPILED = os.path.join(BASE_DIR, STATIC_FOLDER, FILE_NAME)
    _df = pd.read_csv(PATH_COMPILED, encoding="iso-8859-1", low_memory=False)
    return _df

def describeDataField(DESC_FILE_NAME = 'fire_data_description.csv', targetIndex_no=6):
    desc_fire_df = csvToDataframe(FILE_NAME='fire_data_description.csv', STATIC_FOLDER='INT_02_PYTHON_PANDAS_FIRE_DATA')
    dict_keys = desc_fire_df['Column Heading']
    dict_values = desc_fire_df['Value Description']
    _dict = dict(zip(dict_keys, dict_values))
    _listKeys = list(_dict.keys())
    print()
    print("--- all fields of the dataset provided for study assignment: ")
    print(list(_listKeys))
    print()
    print("--- a brief description for target field for data visualization: ")
    _fieldName = _listKeys[targetIndex_no]
    print(str(_fieldName) + "\t " + _dict[_fieldName])
    print()
    return None

describeDataField()

def fireTypeCounter(FIRE_DATA_FILENAME = 'fire_county_data.csv', targetColumn_no=6):
    masterFire_df = csvToDataframe(FIRE_DATA_FILENAME, STATIC_FOLDER='INT_02_PYTHON_PANDAS_FIRE_DATA')
    print("--- a quick peek at dataframe: ")
    print(masterFire_df.head())
    _column_list = (masterFire_df.columns)
    _targetField = _column_list[targetColumn_no]
    print("--- now count only sub type of 18,415 incident: ")
    miniFire_df = masterFire_df[[
        _targetField, 
        'Incident Number'
        ]]
    print(miniFire_df.head())
    fireTypeCount_df = miniFire_df.groupby(_targetField).count().sort_values(by=['Incident Number'], ascending=False)
    print(fireTypeCount_df)
    return fireTypeCount_df.T


def pieMakerFireType(_df=fireTypeCounter()):
    pass
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        
    labels = [str(column) for column in list(_df.columns)]
    print(labels)
    print(len(labels))
    sizes = [ int(size) for size in list(_df.T['Incident Number'])]
    print(sizes)
    print(len(sizes))

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.legend(loc='best')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.style.use('fivethirtyeight')
    plt.rcParams['font.size'] = 8
    ax1.legend(frameon= False)
    # print(plt.rcParams.keys())
    plt.show()
    return None


pieMakerFireType()
