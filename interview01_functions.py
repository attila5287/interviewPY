import os 
import pandas as pd


def bringStateList():
    # need 'os' operating system module to generate file path thus code runs on any pc
    BASE_DIR = os.getcwd() # base directory has the script/code
    FILE_NAME_RJCT = 'loan_declines.csv' # constant for file name>merge for absolute path
    PATH_ABS_REJECTED = os.path.join(BASE_DIR, FILE_NAME_RJCT) 
    rejected_df = pd.read_csv(PATH_ABS_REJECTED).sort_values(by='State',ascending=True)
    _out_list = list(rejected_df['State'].unique())
    return _out_list

bringStateList()


def makeEmallRain():
    """
    MODIFIED, FASTER VERSION OF makeEmRain() COMBINED WITH problem_1() 
    READS CSV FILE OF REJECTED 755K-ROW LOAN APPLICATIONS
    GROUPS DATA BY STATE AND RETURNS MEDIAN DEBT-TO-INCOME RATIO
    FOR ALL STATES. NO PARAMETERS REQ'D RETURNS NONE. PROMPT ONLY
    """
    # need 'os' operating system module to generate file path thus code runs on any pc
    BASE_DIR = os.getcwd() # base directory has the script/code
    FILE_NAME_RJCT = 'loan_declines.csv' # constant for file name>merge for absolute path
    PATH_ABS_REJECTED = os.path.join(BASE_DIR, FILE_NAME_RJCT) 
    rejected_df = pd.read_csv(PATH_ABS_REJECTED)
    full_column_list = rejected_df.columns # need to locate debt2income ratio column
    target_col = str(full_column_list[4])  # lets assign a variable to be on the safe side
    mini_rej_df = rejected_df[[target_col, 'State']]
    mini_rej_df['numbers_str'] = [percentage[:-1] for percentage in mini_rej_df[target_col]]
    mini_rej_df['debt2incomeRatio'] = pd.to_numeric(mini_rej_df['numbers_str'])
    state_med1an_df = pd.DataFrame(mini_rej_df.groupby('State').median())
#     print(state_med1an_df.index)
    print(" ================ DESCRIPTION ----------------- ")
    print(state_med1an_df.describe())
    print(" =========== STATE-DEBT-TO-IN-RAT-MEDIAN ------ ")
    print(state_med1an_df['debt2incomeRatio'])
    print("  --------------- ================ ")
    return None


makeEmallRain()