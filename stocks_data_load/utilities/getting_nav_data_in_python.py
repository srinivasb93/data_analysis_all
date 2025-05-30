import pandas as pd
from mftool import Mftool
from datetime import datetime, timedelta
from mf_data_load.mf_hist_data_load import engine

try:
    conn = engine.connect()
except ConnectionError:
    print('Job aborted due to SQL Server connection issue')


mf = Mftool()

# Getting the scheme codes of mutual funds
scheme_codes = mf.get_scheme_codes()
print(scheme_codes)
exit()

# Uncomment this code when you need to load all scheme codes in DB
"""
df = pd.DataFrame.from_dict(scheme_codes, orient='index').reset_index()
df.columns = ['scheme_code', 'scheme_name']
df.to_sql(name='MF_SCHEME_CODES', con=conn, if_exists='replace', index=False)
"""

my_funds = ['122639', '118834', '118269', '125307', '118778', '125497', '113269']

# getting only the scheme codes from the dictionary.
scheme_code_list = [x for x in scheme_codes.keys() if x in my_funds]

# print(mf.get_scheme_historical_nav('122639', as_Dataframe=True))

def HistoricalNav(scheme_code_list, start_date, end_date):
    # Assert keyword is a debugging tool.
    # Below assert keyword check whehther the scheme_code_list is a list and it is present,
    # if not it raises an assertion failure message.
    assert (isinstance(scheme_code_list, list) is True), "Arguement scheme_code_list should be a list"
    assert (isinstance(start_date, str) is True), "start_date must be a str in %d-%m-%Y format" # checks whether start date is present and is in correct format.
    assert (isinstance(end_date, str) is True), "end_date must be a str in %d-%m-%Y format" # checks whether end date is present and is in correct format

    for scheme_code in scheme_code_list:
        df = mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)
        # df = mf.history(schemes, 'max', as_dataframe=True)  # requesting NAV data from the api.
        # df = mf.history(schemes, start_date, end_date, 'max', as_dataframe=True)
        # # adding Pandas Series(scheme_code) as a column in Pandas Dataframe.
        # df['scheme_code'] = pd.Series([df['scheme_code'] for x in range(len(df.index))])
        # # adding Pandas Series(scheme_name) as a column in Pandas Dataframe.
        # df['scheme_name'] = pd.Series([df['scheme_name'] for x in range(len(df.index))])

        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df.sort_values(by='date', inplace=True)  # sorting the values of every Scheme code based on Date
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        df['dayChange'] = round(df['nav'].pct_change(periods=1)*100, 1)
        df['Change_5days'] = round(df['nav'].pct_change(periods=5)*100, 1)
        df['Change_20days'] = round(df['nav'].pct_change(periods=20)*100, 1)
        scheme_name = scheme_codes.get(scheme_code).split("-")[0].strip().replace(" ", "_")
        df.to_sql(name=scheme_name, con=conn, if_exists='replace', index=False)
        print(f'Data load is complete for {scheme_name}')
    #     main_df = main_df.append(df)  # appending the data in the main_df dataframe.
    #
    # main_df = main_df[['scheme_code', 'scheme_name', 'date', 'nav']]  # creating names of dataframe columns
    # main_df.reset_index(drop=True, inplace=True)
    #
    # return main_df  # Returning the required Dataframe.


# Function to return NAV data 
def NAV_Data(start, end):
  try:
    values_df = HistoricalNav(scheme_code_list=scheme_code_list, start_date=start, end_date=end)  # to get the data
    return values_df
  except KeyError:
    # if the data is not available on that date, going on previous date to get latest data
    start = datetime.strptime(start, '%d-%m-%Y') - timedelta(1)  # gets to previous day where the data is available.
    return NAV_Data(start.strftime("%d-%m-%Y"), end)  # returns the required data.

# Calling the function and saving the output in a variable.
# To get the latest NAV set the start_date and end_date as the last traded date in 'dd/mm/yyyy' format.
# Note:- To get data of a particular date, enter same start_date and end_date. 

start_date = "01-01-2010"  # enter the date in "dd-mm-yyyy" format
end_date = "29-06-2023"  # enter the date in "dd-mm-yyyy" format
values_df = NAV_Data(start_date, end_date)  # calling function NAV_Data


# to get the information about a particular scheme code.
# for scheme in scheme_code_list:
#   values_df = values_df[values_df['scheme_code'] == scheme]
#   scheme_name = scheme_codes.get(scheme).split("-")[0].strip().replace(" ", "_")
#   values_df.to_sql(name=scheme_name, con=conn, if_exists='replace', index=False)
#   print(f'Data load is complete for {scheme_name}!!!')

