import os 
import pandas as pd

def smoothPathCompiler():
    """"
    RETURNS STRING THAT STORES PATH FOR CSV-JSON TO BE READ
    """
    BASE_DIRECTORY = os.getcwd()          # current-working-directory (CONSTANT)
    FILE_NAME_CSV = 'loan_declines.csv'   # csv file name another CST
    # STATIC_FOLDER = '' # if file was a folder like static/images etc. 
    PATH_COMPILED = os.path.join(BASE_DIRECTORY,FILE_NAME_CSV)
    file_type = str(FILE_NAME_CSV[-3:])
    print()
    print("-------------smoothPathCompiler---------------")
    print("extracting data from "+ file_type.upper() +  " file in following path:")
    print(PATH_COMPILED)
    print("----------------------------------------------")
    return str(PATH_COMPILED)

def bringStateList():
    # need 'os' operating system module to generate file path thus code runs on any pc
    BASE_DIR = os.getcwd() # base directory has the script/code
    FILE_NAME_RJCT = 'loan_declines.csv' # constant for file name>merge for absolute path
    PATH_ABS_REJECTED = os.path.join(BASE_DIR, FILE_NAME_RJCT) 
    rejected_df = pd.read_csv(PATH_ABS_REJECTED).sort_values(by='State',ascending=True)
    _out_list = list(rejected_df['State'].unique())
    return _out_list

bringStateList()


def makeEmRain():
    """"
    *** EXTREMELY TIME CONSUMING- NOT RECOMMENDED ***
    RUNS problem_1(state) FUNCTION FOR ALL STATES IN DATASET
    RETURNS NONE PRINTS 
    """
    state_list = bringStateList()
    for state in state_list:
        problem_1(state)
    return None

def makeEmallRain():
    """
    MODIFIED, FASTER VERSION OF makeEmRain() COMBINED WITH problem_1() 
    READS CSV FILE OF REJECTED 755K-ROW LOAN APPLICATIONS -ONLY-ONCE!-
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
    print("  --------------------- ======================= ")
    return None


# makeEmallRain()


def makeEmAllRainFmt():
    pass
    file_path_compiled = smoothPathCompiler()    
    _df = pd.read_csv(file_path_compiled)
    _df = _df[['State','Debt-To-Income Ratio']] #get rid of all other columns
    debt_column = _df['Debt-To-Income Ratio'] # useless str format
    _df['debt2income'] = [debt_element[:-1] for debt_element in debt_column] # still useless
    _df['debt2income'] = pd.to_numeric(_df['debt2income'])  # now its float =)
    debt_col_mod = pd.to_numeric(_df['debt2income'])
    _df = _df[['State', 'debt2income']]
    _df = _df.groupby('State').median()['debt2income']
    _df.sort_values(by='debt2income',ascending=False)
    print("_State_________debt2income_")
    for _state in _df.index:
        _out_debt = _df[_state]
        _out_debt=_out_debt*.01
        print(_state," : \t\t","{:,.2%}".format(_out_debt))
    # __out = _df['debt2income']
    # print(__out)
    return None

# ========================================================

makeEmAllRainFmt()

