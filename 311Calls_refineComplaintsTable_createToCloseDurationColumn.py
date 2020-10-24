import pandas
import numpy as np

year = 2010

# Set up dataframes from relevant tables

# The following paths are not real, they have been amended from the original code for privacy purposes
complaints_fileName = "311Calls_" + str(year) + ".csv"
complaints_tables_directory = "CitadelDataOpen/Complaints Tables/311CensusProcessedData/"
gentr_criteria_filePath = "CitadelDataOpen/datasets/test_one__test_two.csv"
zip_tract_filePath = "CitadelDataOpen/Complaints Tables/zip_tract.csv"
tract_zip_filePath = "tract_zip_2018.csv"

df_gentrCrit = pandas.read_csv(gentr_criteria_filePath, index_col='geoid')

df_311Calls = pandas.read_csv(complaints_tables_directory + complaints_fileName)
df_311Calls.columns = ['key', 'str_createdDate', 'str_closedDate', 'zip']
df_311Calls['createdDate'] = pandas.to_datetime(df_311Calls['str_createdDate'], format="%Y-%m-%d %H:%M:%S")
df_311Calls['closedDate'] = pandas.to_datetime(df_311Calls['str_closedDate'], format="%Y-%m-%d %H:%M:%S")
df_311Calls = df_311Calls.drop(['str_createdDate', 'str_closedDate'], axis=1)
print(df_311Calls.columns)

df_geoid_zip = pandas.read_csv(tract_zip_filePath, usecols=['tract', 'zip'])
df_geoid_zip.columns = ['geoid', 'zip']

df_gentrCrit['zip'] = list(df_geoid_zip[df_geoid_zip.geoid == geoID].zip.iloc[0] for geoID in df_gentrCrit.index)
uniqueZips = np.intersect1d(np.unique(df_gentrCrit.zip), np.unique(df_geoid_zip.zip))
complaintZips = df_311Calls['zip'].to_numpy()

df_infoByZip = pandas.DataFrame({'num_complaints' : np.zeros(len(uniqueZips)), 'avg_closure_time' : np.zeros(len(uniqueZips)), 'num_tracts' : np.zeros(len(uniqueZips)), 'num_gentr_eligible_tracts' : np.zeros(len(uniqueZips)), 'num_test_2_tracts' : np.zeros(len(uniqueZips)), 'num_gentrified_tracts' : np.zeros(len(uniqueZips))}, index=uniqueZips)
# df_infoByZip is indexed by 'zip'
for i in range(len(uniqueZips)):
    zip = uniqueZips[i]

    if complaintZips.__contains__(zip): # If anyone living in the zip has complained before then...
        dfslice_complaintsOfZip = df_311Calls[df_311Calls.zip == zip]
        numComplaints = len(dfslice_complaintsOfZip)
        df_infoByZip.loc[zip, 'num_complaints'] = numComplaints
        df_infoByZip.loc[zip, 'avg_closure_time'] = (dfslice_complaintsOfZip['closedDate'].mean() - dfslice_complaintsOfZip['createdDate'].mean()).seconds // 3600 # hours

        tractArray = np.intersect1d(df_geoid_zip[df_geoid_zip.zip == zip].geoid.to_numpy(), df_gentrCrit.index.to_numpy())
        dfslice_gentrCrit_underZip = df_gentrCrit.loc[tractArray]
        df_infoByZip.loc[zip, 'num_tracts'] = len(tractArray)
        df_infoByZip.loc[zip, 'num_gentr_eligible_tracts'] = len(dfslice_gentrCrit_underZip[dfslice_gentrCrit_underZip.gentrify_elig == 1])
        df_infoByZip.loc[zip, 'num_test_2_tracts'] = len(dfslice_gentrCrit_underZip[dfslice_gentrCrit_underZip.test_two == 1])
        df_infoByZip.loc[zip, 'num_gentrified_tracts'] = len(dfslice_gentrCrit_underZip[dfslice_gentrCrit_underZip.gentrified == 1])
    else:
        df_infoByZip.loc[zip, 'num_complaints'] = 0
        df_infoByZip.loc[zip, 'avg_closure_time'] = 0
        df_infoByZip.loc[zip, 'num_tracts'] = 0
        df_infoByZip.loc[zip, 'num_gentr_eligible_tracts'] = 0
        df_infoByZip.loc[zip, 'num_test_2_tracts'] = 0
        df_infoByZip.loc[zip, 'num_gentrified_tracts'] = 0

df_infoByZip['proportion_gentr_eligible_tracts'] = df_infoByZip.num_gentr_eligible_tracts / df_infoByZip.num_tracts

# correlation between individual columns

print('\nCorr(proportion of gentr_eligible tracts, num_complaints) = ' + str(df_infoByZip.proportion_gentr_eligible_tracts.corr(df_infoByZip.num_complaints)))
print('Corr(proportion of gentrified tracts, num_complaints) = ' + str(df_infoByZip.num_gentrified_tracts.corr(df_infoByZip.num_complaints)))
print('Corr(proportion of gentr_eligible tracts, avg_closure_time) = ' + str(df_infoByZip.proportion_gentr_eligible_tracts.corr(df_infoByZip.avg_closure_time)))
print('Corr(proportion of gentrified tracts, avg_closure_time) = ' + str(df_infoByZip.num_gentrified_tracts.corr(df_infoByZip.avg_closure_time)))