import warnings; warnings.simplefilter('ignore')
import pandas as pd
import os
import datetime as dt

from interview01_functions import (
    smoothPathCompileR,
    smoothPathCompiler
)

# THIS TIME TRYING TO CODE THE SIMPLEST TO WRITE/FASTEST TO RUN FUNCTION FOR COMPETITIVE EDGE ON INT'V
def problem_2_mod(date_first = '2011-01', date_second = '2011-04', prompt_master = False, dict_final = False):
    """
    - Accepts a date range and returns a dictionary of the percentage of loans approved over that time period.
    - Aggregates results by month, and includes the entire month if any part of it is in the request. 
    - For example: problem_2('2011-1-5','2011-1-7') would consider ALL records for January 2011. 
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
        apr_df = pd.DataFrame()
        apr_df = pd.read_csv(file_path_apr) 
        # print(apr_df.columns) # 145 columns slows us down
        apr_df = apr_df[['issue_d', 'policy_code']].dropna() # now two columns
        # print(apr_df.__len__) # 42,542 rows to 42,535 rows * DROPPED 7 na ROWS *
        apr_df = apr_df.groupby('issue_d').count().reset_index()
        apr_df['year_month_dt'] = [dt.datetime.strptime(month_year,'%b-%y') for month_year in apr_df['issue_d']]
        apr_df.set_index('year_month_dt', inplace=True) #move dT column to index
        apr_df.sort_index(inplace=True) #sort from earliest date to latest
        apr_df.drop(columns=['issue_d'], inplace=True)
        apr_df = apr_df.rename(columns={'policy_code':'c0unt'})
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
    # approved_df = approvedDataFramer(prompt_results=True)
    # approved_df = approvedDataFramer()
    # print(approved_df[date_first:date_second]['policy_code'])
    # -----------------------------------------------------------

    def rejectedDataFramer(prompt_results=False):
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
        rej_df = rej_df.rename(columns={'Policy Code':'c0unt'})
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
    
    # # info abt dataframe first and last rows etc. if set True
    
    def list_all_results(prompt_results=False):
        approved_df = approvedDataFramer(prompt_results=True)
        rejected_df = rejectedDataFramer(prompt_results=True)

        # try extracting first digits of timestamp and use str instead of datetime
        date_list_timestamps = list(approved_df[date_first:date_second]['c0unt'].index)
        date_list_string = [ str(date_secondStr)[:10] for date_secondStr in date_list_timestamps]
        date_display_list = [ date[:7] for date in date_list_string ]

        # count of applications approved
        appCount_list = list(approved_df[date_first:date_second]['c0unt'])
        # count of applications rejected
        rejCount_list = list(rejected_df[date_first:date_second]['c0unt'])
        # total count of loan applicants
        total_list = [
            int(appCount+rejCount) for appCount, rejCount in zip(appCount_list,rejCount_list)
        ]
        # percentage of loans approved
        ratioApproved_list = [
            float(appCount/totalCount).__round__(2) for appCount, totalCount in zip(appCount_list, total_list)
        ]
        # percentage of loans rejected
        ratioRejected_list = [
            float(rejCount/totalCount).__round__(2) for rejCount, totalCount in zip(rejCount_list, total_list)
        ]
        print()
        print("date as yr-mo:")
        print(date_display_list) # preferred since easier to work with
        print()
        print("approved loans:")
        print(ratioApproved_list)
        print()
        print("rejected loans:")
        print(ratioRejected_list)
        print()
        print("approved loans: ")
        print(appCount_list)
        print()
        print("rejected applications:")
        print(rejCount_list)
        print()

        final_results_listed = []
        final_results_listed.append(date_display_list)
        # final_results_listed.append(date_list_string)
        final_results_listed.append(ratioApproved_list)
        final_results_listed.append(appCount_list)
        final_results_listed.append(ratioRejected_list)
        final_results_listed.append(rejCount_list)
        final_results_listed.append(total_list)
        return final_results_listed

    _master_list = []
    _master_list = list_all_results()

    if prompt_master == True:
        for i in range(len(_master_list[1])):
            print()
            print("Yr-Mth:     {}".format(_master_list[0][i]))
            print(" - Approved")
            print("     |percentage: {:,.0%}".format(_master_list[1][i]))
            print("     |{:,} of {:,}".format(_master_list[2][i],_master_list[5][i]))
            print(" - Rejected")
            print("     |percentage: {:,.0%}".format(_master_list[3][i]))
            print("     |count {:,} of {:,}".format(_master_list[4][i],_master_list[5][i]))
            print()            
    else:
        pass

        

    if dict_final == True:
        _master_list = list_all_results()
        for i in range(len(_master_list[1]) - 1):
            
            out_keyDate = "{}".format(_master_list[0][i])
            out_appPerc = "{:,.0%}".format(_master_list[1][i])
            out_appCnt = "{:,}".format(_master_list[2][i])
            out_rejPerc = "{:,.0%}".format(_master_list[3][i])
            out_rejCnt = "{:,}".format(_master_list[4][i])
            out_totalCnt = "{:,}".format(_master_list[5][i])
            
            dictFinal = {
                'Date' : out_keyDate,
                'Approved_Ratio' : out_appPerc,
                'Num_LoansApproved' : out_appCnt,
                'Rejected_Ratio' : out_rejPerc,
                'Num_LoansRejected' : out_rejCnt,
                'Num_LoansTotal' : out_totalCnt
            }
            print(dictFinal)
        return dictFinal
    else:
        pass


    return _master_list
# -----------------------------------------
# -----------------test--------------------
returns_dict = problem_2_mod(prompt_master=True, dict_final=True)
# -----------------------------------------
print(type(returns_dict))

