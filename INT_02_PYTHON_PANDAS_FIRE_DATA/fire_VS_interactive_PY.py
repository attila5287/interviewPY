import warnings
warnings.filterwarnings('ignore')
import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def csvToDataframe(FILE_NAME='fire_county_data.csv', STATIC_FOLDER=''):
    """ RETURNS PANDAS DATAFRAME, REQUIRES FILENAME WITH .CSV EXTENSION 
    ALSO STATIC_FOLDER IF ANY DEFAULT NONE """
    BASE_DIR = os.getcwd()
    PATH_COMPILED = os.path.join(BASE_DIR, FILE_NAME)
    _df = pd.read_csv(PATH_COMPILED, encoding="iso-8859-1", low_memory=False)
    return _df

csvToDataframe()

def describeFireData(DESC_FILE_NAME = 'fire_data_description.csv'):
    desc_fire_df = csvToDataframe(DESC_FILE_NAME)
    dict_keys = desc_fire_df['Column Heading']
    dict_values = desc_fire_df['Value Description']
    _dict = dict(zip(dict_keys, dict_values))
    print(_dict)
    return None

describeFireData()

def ctgryResptimeDataFramer(FIRE_DATA_FILENAME = 'fire_county_data.csv'):
    fire_df = csvToDataframe(FIRE_DATA_FILENAME, STATIC_FOLDER='/INT_02_PYTHON_PANDAS_FIRE_DATA/')
    responseTime_df = fire_df[['Property Use Category', 'Total First Unit Response Time']].dropna()
    responseTime_df['responseTime'] = responseTime_df['Total First Unit Response Time']
    responseTime_df.drop(columns='Total First Unit Response Time', inplace=True)

    # groupby -> mean doesnot work yet. dtype is non-numeric
    responseTime_df['responseTim3'] = [ int(int(dt.datetime.strptime(response,'%H:%M:%S').hour)*3600 + int(dt.datetime.strptime(response,'%H:%M:%S').minute)*60 + int(dt.datetime.strptime(response,'%H:%M:%S').second))
        for response in responseTime_df['responseTime']
    ]
    resPrpCtgFocused_df = responseTime_df.groupby('Property Use Category').mean().__round__(0)
    resPrpCtgFocused_df['responseTim3'] = [int(second) 
                                                    for second in resPrpCtgFocused_df['responseTim3']
                                                ]
    resPrpCtgFocused_df.sort_values(by= ['responseTim3'], ascending=False, inplace=True)
    resPrpCtgFocused_df=resPrpCtgFocused_df.T
    _df = resPrpCtgFocused_df.copy()
    keys_list = [str(column) for column in list(_df.columns)]
    values_list = [_df[column] for column in keys_list]
    return _df

#     ctgryResptimeDataFramer()

def barCategoryRespTimer(_df = ctgryResptimeDataFramer()):
    _list = list(_df.columns)
    plt.style.use(style='fivethirtyeight')
    plt.figure(figsize=(8,6))
    plt.grid(True)
    plt.title("Response Time vs Property Use Category")
    plt.xlabel('Response Time In Seconds')
    plt.rcParams['font.size'] = 14
# parameter: create an axis with all around average
    for category in _list:
        plt.barh(category[:12], _df[category],alpha = 0.75, align='center', label=category)
#     plt.legend(loc='best')
    plt.show()
    return None

barCategoryRespTimer()
    
# ===============================
print('TASK COMPLETED')

