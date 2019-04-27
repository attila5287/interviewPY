import os
import pandas as pd
import datetime as dt 
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from functions_of_fire import(csvToDataframe, describeDataField)
# simple warnings OFF
import warnings; warnings.simplefilter('ignore')


# ['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']

describeDataField(targetIndex_no=8)

def monthlyIncidentCounter(FIRE_DATA_FILENAME = 'fire_county_data.csv', targetColumn_no=8):
    masterFire_df = pd.DataFrame()
    _df = pd.DataFrame()
    masterFire_df = csvToDataframe(FIRE_DATA_FILENAME, STATIC_FOLDER='INT_02_PYTHON_PANDAS_FIRE_DATA')
    print()
    print(" -------part4:LINE-CHART------ ")
    print()
    # lets automate the process by user input instead of manual/optional
    _column_list = (masterFire_df.columns) 
    _targetField = _column_list[targetColumn_no] 
    _df = masterFire_df[[_targetField,  'Sub Type Category', 'Incident Number']] 
    # add a column of datetime objects, drop timestamp column
    _df['dat3only'] = [ pd.to_datetime(timest4mp).replace(day=1).date() for timest4mp in _df[_targetField]]
    _df = _df.drop(columns=['Incident Date and Time'])
    _df = _df.groupby(['dat3only','Sub Type Category']).count().reset_index()
    _df = _df.pivot(
        index='dat3only',
        columns='Sub Type Category',
        values = 'Incident Number'
    ).fillna(0)
    _finalCol_list = list(_df.columns)



    label_list = []
    for column in _finalCol_list:
        _df[column] = _df[column].astype(dtype=int, inplace=True)
        plt.plot(_df.index,_df[column], linewidth=0.5, marker = 'o', label = column)
        plt.legend(loc = 'best')
    plt.show()

    plt.figure(figsize=(25,15))
    plt.rcParams["font.size"] = 10
    plt.grid(True)
    plt.title("Number of Incidents vs Month for 2016-2017")
    # plt.xlabel("Year")
    plt.ylabel(" Number of Incidents ")

    # for state in stateMeanYear_pdf.columns:
    # plt.plot(stateMeanYear_pdf.index, stateMeanYear_pdf[state], linewidth=1, linestyle='--', marker = 'o',label=state)
    # plt.legend(loc='best')
    # plt.show()


    # ------------------------------------------
    _out = _df.copy()
    print(_out.head()) 
    return _out

def monthlyIncidentLineCharter(_df = monthlyIncidentCounter(FIRE_DATA_FILENAME = 'fire_county_data.csv', targetColumn_no=8)):
    x_axis = _df.index[:11]
    y_axis = _df['Incident Number'][:11]
    
    plt.plot(x_axis, y_axis, marker='o', )    
    plt.show()



    return None


# monthlyIncidentLineCharter()