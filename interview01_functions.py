import os 
import pandas as pd


def bringStateList():
    # need 'os' operating system module to generate file path thus code runs on any pc
    BASE_DIR = os.getcwd() # base directory has the script/code
    FILE_NAME_RJCT = 'loan_declines.csv' # constant for file name>merge for absolute path
    PATH_ABS_REJECTED = os.path.join(BASE_DIR, FILE_NAME_RJCT) 
    rejected_df = pd.read_csv(PATH_ABS_REJECTED)
    _out_list = list(rejected_df['State'].unique())
    return _out_list