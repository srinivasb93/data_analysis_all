import pandas as pd
import sqlalchemy as sa
import urllib.parse
import os

# Use this for windows authentication
database = 'NSEDATA'
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=IN01-9MCXZH3\SQLEXPRESS;"
                                 f"DATABASE={database};"
                                 "Trusted_Connection=yes")
'''
#Use this for SQL server authentication
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=IN01-9MCXZH3\SQLEXPRESS;"
                                 "DATABASE=test;"
                                 "UID=user;"
                                 "PWD=password")
'''

# Connection String
engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Connect to the required SQL Server
conn = engine.connect()

file_name_with_path = r"C:\Users\sba400\OneDrive - Cambium Networks Limited\Desktop\My Reports.xlsx"

table_name = "ALL_STOCKS"
file_data = pd.read_excel(file_name_with_path, parse_dates=True, sheet_name='Equity')
# Load file data to SQL Table
file_data.to_sql(stock, con=conn, if_exists='replace', index=False)
print('Data Load is complete for stock : {}'.format(stock))

