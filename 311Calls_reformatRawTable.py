import pandas
import numpy as np

filename = "311Calls_2018.csv"
path_311Calls = "/Volumes/extMac/Downloads/" + filename
savePath = "/Volumes/extMac/Desktop/CitadelDataOpen/Complaints Tables/311CensusProcessedData/" + filename
df_311Calls = pandas.read_csv(path_311Calls, usecols=[0, 1, 2, 8], dtype={'Unique Key' : str, 'Created Date' : str, 'Closed Date' : str, 'Incident Zip' : str })
df_311Calls.columns = ['key', 'str_createdDate', 'str_closedDate', 'raw_str_zip']
df_311Calls = df_311Calls.dropna()
df_311Calls['createdDate'] = pandas.to_datetime(df_311Calls['str_createdDate'], format="%m/%d/%Y %I:%M:%S %p")
df_311Calls['closedDate'] = pandas.to_datetime(df_311Calls['str_closedDate'], format="%m/%d/%Y %I:%M:%S %p")
df_311Calls['fzip'] = pandas.to_numeric(df_311Calls['raw_str_zip'].str[:5], errors='coerce')
df_311Calls = df_311Calls.drop(['raw_str_zip', 'str_createdDate', 'str_closedDate'], axis=1)
df_311Calls = df_311Calls.dropna()
df_311Calls['zip'] = df_311Calls['fzip'].astype(int)
df_311Calls = df_311Calls.drop(['fzip'], axis=1)
df_311Calls.to_csv(savePath, index=False)