import pandas as pd
import os
import datetime as dt

from interview01_functions import (
    smoothPathCompileR,
    smoothPathCompiler
)

# THIS TIME TRYING TO CODE THE SIMPLEST TO WRITE/FASTEST TO RUN FUNCTION FOR COMPETITIVE EDGE ON INT'V
def problem_2_mod(date_first = '2011-01', date_second = '2011-04'):
    """
    - Accepts a date range and returns a dictionary of the percentage of loans approved over that time period.
    - Aggregates results by month, and includes the entire month if any part of it is in the request. 
        For example: problem_2('2011-1-5','2011-1-7') would consider ALL records for January 2011. 
    - Assumes that loans are immediately approved/funded upon application 
        (eg. Application date/ fund date/ decline date are all equivalent.) 
    - Example call, response: problem_2(‘2011-1-2’, ‘2011-4-5’) might return
    {‘2011/1/1’ : 0.091 , ‘2011/2/1’ :  0.081, ‘2011/3/1’ :  0.074, ‘2011/4/1’ : 0.082}
    """
    def approvedDataFramer(prompt_results=False):
        """
        RETURNS A TAILOR-MADE DATAFRAME AS PER ASSIGNMENT REQUIREMENTS
        PERFORMS ALL NECESSARY OPERATIONS: I.E.READS CSV FOR 42K-ROW/145-COL
        DATASET, DROPS COLS NANS, CREATE DATETIME THEN SETS TO INDEX
        """
        file_path_apr = smoothPathCompileR() # this is a little cheesy since the function is tailor-made
        apr_df = pd.read_csv(file_path_apr) 
        # print(apr_df.columns) # 145 columns slows us down
        apr_df = apr_df[['issue_d', 'policy_code']].dropna() # now two columns
        # print(apr_df.__len__) # 42,542 rows to 42,535 rows * DROPPED 7 na ROWS *
        apr_df = apr_df.groupby('issue_d').count().reset_index()
        apr_df['dateTime'] = [dt.datetime.strptime(month_year,'%b-%y') for month_year in apr_df['issue_d']]
        apr_df.set_index('dateTime', inplace=True) #move dT column to index
        apr_df.sort_index(inplace=True) #sort from earliest date to latest
        apr_df.drop(columns=['issue_d'], inplace=True)
        def approvedPrompt():
            print()
            print('-------------approvedDataFramer---------------')
            print(apr_df[:3])
            print(' ...  ... ')
            print(apr_df[-3:])
            print()
            print('----------------------------------------------')
            print(apr_df.describe())
            print('----------------------------------------------')
            print()             
            return None
        
        if prompt_results==True:
            approvedPrompt()
        else:
            pass
        
        return apr_df
    approved_df = approvedDataFramer(prompt_results=True)
    print(approved_df[date_first:date_second]['policy_code'])
    # -----------------------------------------------------------

    def rejectedDataFramer(date_rej1='2011-01', date_rej2='2011-04', prompt_results=False):
        """"
        RETURNS A TAILOR-MADE DATAFRAME AS PER ASSIGNMENT REQUIREMENTS
        READS REJECTED LOAN APPLICATIONS DATASET of 755k ROWS        
        """        
        pass
        rej_df= pd.DataFrame()                              #initiate empty df
        file_rejected_csv = smoothPathCompiler()            #uses os please see _functions.PY           
        rej_df = pd.read_csv(file_rejected_csv)             #huge dataframe with a 3/4 of a million rows
        # first move is to decrease row number, remember 1 accepted loans 0 rejected loans so not sum()
        rej_df = rej_df[['Application Date','Policy Code']].groupby('Application Date').count().dropna()
        rej_df = rej_df.reset_index() #still need that data column for conversion to datetime object
        #below is somehow needed otherwise it gives error msg
        rej_df['appDate_string'] = [
            str(date) for date in rej_df['Application Date']
        ]
        # now need to parse date in strings to datetime objects in order to sort by date
        rej_df['appDate_dt'] = [dt.datetime.strptime(date,'%m/%d/%Y') for date in rej_df['appDate_string'] ]
        
        #  
        rej_df['year_month_Str'] = [str(fullDate)[:7]+"-01" for fullDate in rej_df['appDate_dt']]
        rej_df = rej_df.groupby('year_month_Str').sum().reset_index().dropna()


        rej_df['year_month_dt'] = [
             dt.datetime.strptime(yearMonthString,'%Y-%m-%d') for yearMonthString in rej_df['year_month_Str']
        ]
        rej_df = rej_df.set_index('year_month_dt')[['Policy Code']]

        def rejectedPrompt():
            print()
            print('-------------rejectedDataFramer---------------')
            print(rej_df[:3])
            print(' ...  ... ')
            print(rej_df[-3:])
            print()
            print('----------------------------------------------')
            print(rej_df.describe()) 
            print('----------------------------------------------')
            print()             
            return None

        if prompt_results == True:
            rejectedPrompt()
        else:
            pass

        return rej_df



    rejected_df = rejectedDataFramer(prompt_results=True)
    return None
# -----------------test--------------------
problem_2_mod() 

# test_date =  '2009-10'
# test_date2 = '2010-02'
# problem_2_mod(test_date, test_date2) 
# -----------------------------------------

