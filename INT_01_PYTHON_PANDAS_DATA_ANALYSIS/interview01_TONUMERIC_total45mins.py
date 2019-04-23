import warnings; warnings.simplefilter('ignore')
import pandas as pd
import datetime as dt
import os 

from interview01_functions import(
    bringStateList,
    makeEmRain,
    makeEmallRain,
    smoothPathCompiler,
    makeEmAllRainFmt
)


# =====================================================================
# 1. Write a function called problem_1, which accepts a state abbreviation (eg 'PA') and returns the median Debt to income ratio of rejected loan applications for that state.
# =====================================================================
def problem_1(state='CO'):
    """
    READS CSV FILE OF REJECTED 755K-ROW LOAN APPLICATIONS
    GROUPS DATA BY STATE AND RETURNS MEDIAN DEBT-TO-INCOME RATIO
    IF NO INPUT GIVEN, DEFAULT STATE IS CO, COLORADO
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
    state_med1an_df = mini_rej_df.groupby('State').median()['debt2incomeRatio']
    state_med1an = state_med1an_df[state]
    _out_prompt = str("Median for " + state + " state Debt-to-income-ratio is " + str(state_med1an) + " percent")
    print(" ---------------------- ================ ")
    print(_out_prompt)
    print(" ====================== ---------------- ")
    return _out_prompt
# =====================================================================
# problem_1('AK') # TRY WITH USER INPUT
# 'Median for AK state Debt-to-income-ratio is 14.93 percent'

problem_1() # OR NO ARGUMENT NO INPUT AT ALL
# 'Median for CO state Debt-to-income-ratio is 18.48 percent'

# =====================================================================
# 1A. ADVANCED: Write a function called problem_1_advanced() that returns 
# the median Debt to income ratio of rejected loan applications for all states in dataset
# 
# =====================================================================
# FIRST APPROACH: since we have a function that returns for a single state, problem_1 why dont we
# run the same darn thing for all states. huh? 
# 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 
# makeEmRain  *** WRRRRONG! CRAZY-SLOW! READS CSV FOR EVERY SINGLE OUTPUT FOR FIFTY-TWO STATES  ***

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# SECOND APPROACH: lets try to modify problem_1 thus returns debt2incomeRatio for all states
# while performing these calculations with a single read of csv file, in contrary to makeEmRain
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# makeEmallRain() 


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# SECOND APPROACH + COSMETICS = makeEmAllRainFormatted() that returns a list consisting of percentage-style-formatted values for each state
makeEmAllRainFmt()

