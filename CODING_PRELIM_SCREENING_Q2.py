import pandas as pd
import datetime as dt
from datetime import timedelta
import warnings; warnings.simplefilter('ignore')

# dates sent with assignment stored thus named as constansts
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
    # first function is somehow required to use input to be used for indexing
    def adjustDatetime(date_string):
        """
        RETURNS DATE AS STRING FOR DATETIME SERIES FUNC CALLS
        ONLY REQUIRED FOR NEXT FUNCTION METHOD
        """
        _date_string = str(date_string)
        _dt = dt.datetime.strptime(_date_string,'%Y-%m-%d').replace(day=1)
        _dt_date = _dt.date() #date has no time hour min etc. only year month day
        y = _dt_date.year
        m = _dt_date.month
        d = _dt_date.day
        return str(dt.datetime(y, m,d).date())


# this is first step to pull data from a 755 thousand rows dataset
# currently around 40% of total time spent on this step

    def monthlyLoanRejectedDFramer(date_start,date_end):
        """REQUIRES START AND END DATE AS PARAMETERS, 
        RETURNS A DATAFRAME DT-DATE INDEXED GROUPED UNDER MONTHLY FREQ
        //IGNORES DAY ON INPUT DATES AND RETURNS MONTHLY GROUPED REJECTION COUNT AS VALUES// 
        """
        file_path_rej = 'loan_declines.csv'
        dataRejected = pd.read_csv(file_path_rej)
        rejected_df = dataRejected.groupby('Application Date').count().reset_index().dropna()
        rejected_df['ApplicationDate_str'] = [ str(dateApp ) for dateApp in rejected_df['Application Date'] ]
        rejected_df['date_dt'] = [dt.datetime.strptime(dateApp,'%m/%d/%Y') for dateApp in rejected_df['ApplicationDate_str']]
        rejectedmini_df = rejected_df[['Policy Code','date_dt']]
        rejectedmini_df['yearM0nth'] = rejectedmini_df['date_dt'].map(lambda dt: dt.replace(day=1))
        rejectedFinal_df = rejectedmini_df.groupby('yearM0nth').sum()
        date_start_adj = adjustDatetime(date_start)
        return rejectedFinal_df.loc[date_start_adj:date_end]

# this is the second part where we pull csv data for those whose loan application is approved
# this is also the second largest code part with a 30% of the pie
# sample execution in 923ms of 3.01 seconds total time

    def monthlyLoanApprovedDFramer(date_start,date_end):
        """
        REQUIRES START AND END DATE AS PARAMETERS, 
        RETURNS A DATAFRAME DT-DATE INDEXED GROUPED UNDER MONTHLY FREQ
        // NO DAILY BREAKDOWN PROVIDED THUS MONTHLY COUNT ONLY //
        """
        file_path_approved = 'loan_approvals.csv'
        appRaw_df = pd.read_csv(file_path_approved)
        appGrpDate_df = appRaw_df.groupby('issue_d').count().reset_index().dropna()
        approvedMini_df = appGrpDate_df[['issue_d', 'policy_code']]
        approvedMini_df['date_dt'] = [dt.datetime.strptime(issueDate,'%b-%y') for issueDate in appGrpDate_df['issue_d']]
        date_start_adj = adjustDatetime(date_start) #removes the bias-offset
        return approvedMini_df.groupby('date_dt').sum()[date_start_adj : date_end]

    def buildPercAppList(date_zer0, date_aga1n):
        """
        RETURNS A LIST OF PERCENTAGE RATIO FOR LOAN APPLICATIONS
        """
        rej_df = monthlyLoanRejectedDFramer(date_zer0,date_aga1n)
        rejected_list = rej_df['Policy Code']
        app_df = monthlyLoanApprovedDFramer(date_zer0, date_aga1n)
        approved_list = app_df['policy_code']
    # --------------- ---------------
        all_list, perc_formatted_list, percentage_approved_list = [],[],[]
        all_list = [int(approved+rejected) for approved, rejected in zip(approved_list, rejected_list)]
    #  --------------- ---------------
        for approved, total in zip(approved_list,all_list):
            perc_app = int(approved)/int(total)
            percentage_approved_list.append(perc_app)
            perc_formatted = '{:,.1%} '.format(perc_app)
            perc_formatted_list.append(perc_formatted)

        _out = perc_formatted_list
        return _out

    def buildDateListStr(date_zer0, date_aga1n) :
        # first list for dictionary, keys 
        dates_list = monthlyLoanApprovedDFramer(date_zer0, date_aga1n).index
        dates_list_str = dates_list.astype('S')
        return dates_list_str

    def buildFinalDict(date_zer0, date_aga1n):
        dateRange_results =  buildDateListStr(date_zer0, date_aga1n)
        perc_results = buildPercAppList(date_zer0,date_aga1n)

        _out = dict(zip(dateRange_results,perc_results))
#         print(_out)
        return dict(zip(dateRange_results,perc_results))

    _outFnlDict = buildFinalDict(date_start,date_end)
    print(_outFnlDict)
    return _outFnlDict
# ---------------------------------------------------
# --------test with dates sent on assignment --------
problem_2(TEST_STARTDATE, TEST_ENDDATE)