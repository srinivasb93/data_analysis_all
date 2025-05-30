from mftool import Mftool
import nsepy
from nsepy import get_history
from datetime import date,datetime as dt

import sqlalchemy as sa
import urllib.parse
import pandas as pd

mf = Mftool()

#Use this for windows authentication
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=IN01-9MCXZH3\SQLEXPRESS;"
                                 "DATABASE=MFDATA;"
                                 "Trusted_Connection=yes")

'''
#Use this for SQL server authentication
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=dagger;"
                                 "DATABASE=test;"
                                 "UID=user;"
                                 "PWD=password")
'''

#Connection String
engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Connect to the required SQL Server
conn=engine.connect()

"""
# Code to extract and load the scheme name and codes of all MFs
df = pd.DataFrame.from_dict(mf.get_scheme_codes(as_json=False),orient='index')
df.reset_index(inplace=True)
df.columns = ['Code','Scheme_Name']
df.to_sql(name='MF_SCHEME_CODES',con=conn,if_exists='replace',index=False)
"""

query = "SELECT * FROM dbo.MF_SCHEME_DETAILS WHERE SCHEME_CODE IN (135781,120603,119755,118825,118834,120505,120503,118269,146130,118834,118778,\
122639,125307,118791,109445,113177,118825,112932,112323,135783,118825,118834)"

mf_data = conn.execute(query)
mfunds = mf_data.fetchall()
df = pd.DataFrame(mfunds, columns=['fund_house', 'scheme_type', 'scheme_category', 'scheme_code',
                                   'scheme_name', 'scheme_start_date', 'scheme_nav'])

for data in df.itertuples():
    code = data[4]
    print("Extract data for the Fund : {}".format(data[5]))
    # if code != 119550:
    #     continue

    fund_house = data[1].split(' ')[0]
    fund_type = "DIRECT" if "DIRECT" in data[5].upper() else "REGULAR"
    fund_name = data[5].split('-')[0].split(' ')

    fund_name = fund_name[0] + '_' + '_'.join(fund_name[-4:-1])
    fund_name = fund_name.replace('_&_', '_') if '&' in fund_name else fund_name

    tbl_name = fund_name.upper() + f'_{str(code)}_' + fund_type
    df1 = pd.DataFrame()

    try:
        mf_hist_data = mf.get_scheme_historical_nav(code=code, as_Dataframe=True)
    except Exception as e:
        print(e)
        print("Data Load not done for the Fund : {}".format(data[5]))
        continue
    mf_hist_data.reset_index(inplace=True)
    mf_hist_data['date'] = pd.to_datetime(mf_hist_data['date'], format='%d-%m-%Y')
    mf_hist_data['nav'] = mf_hist_data['nav'].astype(dtype=float)
    mf_hist_data['nav'].replace(0, method='pad', inplace=True)
    mf_hist_data.sort_values(by='date', ascending=True, inplace=True)
    mf_hist_data['nav_chg_daily'] = round(mf_hist_data['nav'].pct_change() * 100, 2)
    mf_hist_data['nav_chg_wkly'] = round(mf_hist_data['nav'].pct_change(periods=5) * 100, 2)
    mf_hist_data['nav_chg_mth'] = round(mf_hist_data['nav'].pct_change(periods=20) * 100, 2)

    try:
        mf_hist_data.to_sql(name=tbl_name, con=conn, if_exists='replace', index=False)
    except Exception as e:
        print('error is : {}'.format(e))
        print("Data Load not done for the Fund : {}".format(data[5]))
        continue
    print("Data Load done for the Fund : {}".format(data[5]))

