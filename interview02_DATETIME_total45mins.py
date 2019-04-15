# simple warnings OFF
import warnings; warnings.simplefilter('ignore')

# pandas is required to read big data csv file abt a 3/4 th of a million row
import pandas as pd

# datetime will be used to convert string from csv to date/time series 
import datetime as dt

import os 

# dates sent with assignment named as CONSTANT
TEST_STARTDATE = '2011-1-2'
TEST_ENDDATE = '2011-4-5'

def problem_2(date_start, date_end):
    """
    - Accepts a date range and returns a dictionary of the percentage of loans approved over that time period.
    - Aggregatesresults by month, and includes the entire month if any part of it is in the request. 
        For example: problem_2('2011-1-5','2011-1-7') would consider ALL records for January 2011. 
    - Assumes that loans are immediately approved/funded upon application 
                (eg. Application date/ fund date/ decline date are all equivalent.) 
    - Example call, response: problem_2(‘2011-1-2’, ‘2011-4-5’) might return
    {‘2011/1/1’ : 0.091 , ‘2011/2/1’ :  0.081, ‘2011/3/1’ :  0.074, ‘2011/4/1’ : 0.082}
    """
#-0-this function was somewhat necessary for accurate date conversion
# originally written to deduct a month to fix datetime series index offset
# then it turns out that the best way to work with dt objects is to parse them 
    def adjustDatetime(date_string):
        """
        RETURNS DATE AS STRING FOR DATETIME SERIES FUNC CALLS
        ONLY REQUIRED FOR NEXT FUNCTION METHOD
        """
        _date_string = str(date_string)
        _dt = dt.datetime.strptime(_date_string,'%Y-%m-%d').replace(day=1)
        _dt_date = _dt.date() #date has no time hour min etc. only year month day
        y, m ,d = _dt_date.year, _dt_date.month, _dt_date.day
        return str(dt.datetime(y, m,d).date())

#-I-this is one of the main-duo. Reads the largest file with 755 thousand rows
# returns a dataframe thus would only be used for internal calculations
    def monthlyLoanRejectedDFramer(date_start,date_end):
        """REQUIRES START AND END DATE AS PARAMETERS, 
        RETURNS A DATAFRAME DT-DATE INDEXED GROUPED UNDER MONTHLY FREQ
        //IGNORES DAY ON INPUT DATES AND RETURNS MONTHLY GROUPED REJECTION COUNT AS VALUES// 
        """
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.getcwd()
        FILE_NAME_RJCT = 'loan_declines.csv'
        path_rejected = os.path.join(BASE_DIR, FILE_NAME_RJCT)
        dataRejected = pd.read_csv(path_rejected)
        rejected_df = dataRejected.groupby('Application Date').count().reset_index().dropna()
        rejected_df = rejected_df[['Policy Code', 'Application Date']]
        rejected_df['ApplicationDate_str'] = [ str(dateApp ) for dateApp in rejected_df['Application Date'] ]
        rejected_df['date_dt'] = [
            dt.datetime.strptime(dateApp,'%m/%d/%Y') for dateApp in rejected_df['ApplicationDate_str']
            ]
        rejectedmini_df = rejected_df[['Policy Code','date_dt']]
        rejectedmini_df['yearM0nth'] = rejectedmini_df['date_dt'].map(lambda dt: dt.replace(day=1))
        rejectedFinal_df = rejectedmini_df.groupby('yearM0nth').sum()
        date_start_adj = adjustDatetime(date_start)
        __df = rejectedFinal_df.loc[date_start_adj:date_end]
        return __df
 
#-II- just like above but only reads abt 45 thousand row csv file
# again will mostly be used for internal calc since it returns a dataframe
    def monthlyLoanApprovedDFramer(date_start,date_end):
        """
        REQUIRES START AND END DATE AS PARAMETERS, 
        RETURNS A DATAFRAME DT-DATE INDEXED GROUPED UNDER MONTHLY FREQ
        // NO DAILY BREAKDOWN PROVIDED THUS MONTHLY COUNT ONLY //
        """
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_NAME_APRV = 'loan_approvals.csv'
        file_path_approved = os.path.join(BASE_DIR, FILE_NAME_APRV)
        appRaw_df = pd.read_csv(file_path_approved)
        appGrpDate_df = appRaw_df.groupby('issue_d').count().reset_index().dropna()
        approvedMini_df = appGrpDate_df[['issue_d', 'policy_code']]
        approvedMini_df['date_dt'] = [dt.datetime.strptime(issueDate,'%b-%y') for issueDate in appGrpDate_df['issue_d']
        ]
        date_start_adj = adjustDatetime(date_start) #removes the bias-offset
        return approvedMini_df.groupby('date_dt').sum()[date_start_adj : date_end]

#-III-this function creates a list from above dataframe
#calculates with float as dtype then converts them into -percentage-formatted string 
    def buildPercAppList(date_zer0, date_aga1n):
        """
        RETURNS A LIST OF PERCENTAGE RATIO FOR LOAN APPLICATIONS
        """
# first dataframe, larger one 
        rej_df = monthlyLoanRejectedDFramer(date_zer0,date_aga1n)
# note: count of policy code will give us the number of rejected loan applicants
        rejected_list = rej_df['Policy Code']
# second dataframe, smaller one 
        app_df = monthlyLoanApprovedDFramer(date_zer0, date_aga1n)
# count of policy code will give us number of approved applications
        approved_list = app_df['policy_code']
# will create three blank lists. note =[] is faster than =list()
# all_list stores sum of apprvd+rejected ALL APPLICANTS
# perc_approved stores float dtype of results approval perc
# perc_formatted_list stores RESULTS as string objects in a presentable format
        all_list, perc_formatted_list, percentage_approved_list = [],[],[]
        all_list = [int(approved+rejected) for approved, rejected in zip(approved_list, rejected_list)]
#  block to fill up above created list. dvide approved count/total 
        for approved, total in zip(approved_list,all_list):
            perc_app = int(approved)/int(total)
            percentage_approved_list.append(perc_app)
            perc_formatted = '{:,.1%} '.format(perc_app)
            perc_formatted_list.append(perc_formatted)

        _out = perc_formatted_list
        return _out

    def buildDateListStr(date_zer0, date_aga1n):
        """
        RETURNS A LIST OF MONTHS STORED AS STRING THAT WILL BE
        USED AS KEYS FOR OUTPUT-DICTIONARY
        """
        # first list for dictionary, keys 
        dates_list = monthlyLoanApprovedDFramer(date_zer0, date_aga1n).index
        dates_list_str = dates_list.astype('S')
        return dates_list_str

    def buildFinalDict(date_zer0, date_aga1n):
        """
        RETURNS A DICTIONARY WITH MONTHS THROUGH INPUT-DATE-RANGE AS KEYS
        AND PERC OF LOAN APPLICATIONS APPROVED WITHIN THE MONTH 
        """
        dateRange_results =  buildDateListStr(date_zer0, date_aga1n)
        perc_results = buildPercAppList(date_zer0,date_aga1n)

        _out = dict(zip(dateRange_results,perc_results))
#         print(_out)
        return _out

    def prompt_month_year(date_string):
        """
        PRINTS MESSAGES WHEN FUNCTION CALLED, CONVERTS DATE FROM %m 
        FORMAT TO FULL NAME, GENERATES SIMPLE TEXT AS GENERAL INFO
        """
        _date_string = str(date_string)
        _dt = dt.datetime.strptime(_date_string,'%Y-%m-%d')
        _dt = dt.datetime.strptime(_date_string,'%Y-%m-%d').replace(day=1)
        _dt_date = _dt.date() #date has no time hour min etc. only year month day
        y, m ,d = _dt_date.year, _dt_date.month, _dt_date.day
    # convert month-integer to full name for a better presentation
        _dict = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', 
            '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December' 
        }
        _month = str(dt.datetime(y, m,d).date().month)
        _month_full = _dict[_month]
        _year= str(dt.datetime(y, m,d).date().year)
        _out = _month_full + " of " + _year
        return _out

    
    
    _outFnlDict = buildFinalDict(date_start,date_end)
    
# _______________________ PROMPT-OUTPUT _______________________
    def displayResults():
        """
        RETURNS NONE, REQUIRES NO ARGUMENT, PRINTS 
        """
        __outFnlDict = buildFinalDict(date_start,date_end)
        print() 
        print("------------------ USER INPUT -----------------")
        print("start date  : " + date_start )
        print("end date    : " + date_end )
        print("-------------- AGGREGATE BY MONTH ------------- ")
        print("first month : " + prompt_month_year(date_start))
        print("last month  : " + prompt_month_year(date_end))
        print(" -------------- DICTIONARY - KEYS ------------- ")
        print([__outFnlDict.keys()])
        print(" ------------- DICTIONARY - RESULTS ----------- ")
        print([__outFnlDict.values()])
        print(" -------------- DICTIONARY - PAIRS  ----------- ")
        for pair in _outFnlDict:
            print(pair + " | " + _outFnlDict[pair])
        print(" ------------------ THE-END  ------------------ ")
        print() 
        return None
    
    displayResults()

    return _outFnlDict
# =====================================================================
# problem_2(TEST_STARTDATE,TEST_ENDDATE)
# ------------------ USER INPUT -----------------
# start date  : 2011-1-2
# end date    : 2011-4-5
# -------------- AGGREGATE BY MONTH -------------
# first month : January of 2011
# last month  : April of 2011
#  -------------- DICTIONARY - KEYS -------------
# [dict_keys(['2011-01-01', '2011-02-01', '2011-03-01', '2011-04-01'])]
#  ------------- DICTIONARY - VALUES -----------
# [dict_values(['9.1% ', '8.1% ', '7.5% ', '8.2% '])]
#  -------------- RESULTS - TEST EX  -----------
# 2011-01-01 | 9.1%
# 2011-02-01 | 8.1%
# 2011-03-01 | 7.5%
# 2011-04-01 | 8.2%
#  ------------------ THE-END  ------------------

TEST_STARTDATE0 = '2008-4-6'
TEST_ENDDATE0 = '2009-1-2'


problem_2(TEST_STARTDATE0,TEST_ENDDATE0)

# -------------- AGGREGATE BY MONTH -------------
# first month : April of 2008
# last month  : January of 2009
#  -------------- DICTIONARY - KEYS -------------
# [dict_keys(['2008-04-01', '2008-05-01', '2008-06-01', '2008-07-01', '2008-08-01', '2008-09-01', '2008-10-01', '2008-11-01', '2008-12-01', '2009-01-01'])]
#  ------------- DICTIONARY - RESULTS -----------
# [dict_values(['8.3% ', '8.8% ', '8.4% ', '10.1% ', '7.3% ', '5.4% ', '5.0% ', '6.0% ', '7.2% ', '8.0% '])]
#  -------------- DICTIONARY - PAIRS  -----------
# 2008-04-01 | 8.3%
# 2008-05-01 | 8.8%
# 2008-06-01 | 8.4%
# 2008-07-01 | 10.1%
# 2008-08-01 | 7.3%
# 2008-09-01 | 5.4%
# 2008-10-01 | 5.0%
# 2008-11-01 | 6.0%
# 2008-12-01 | 7.2%

#  ------------------ THE-END  ------------------

