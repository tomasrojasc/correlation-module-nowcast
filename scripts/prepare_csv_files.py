"""
This script takes the raw csv files (file1.csv and file2.csv) and
saves each night as a csv file in the UT_data folder. Each file is a
csv file without headers. The structure for those files is a column
with the julian date and the corresponding seeing measurement.

It also outputs a list of the shared dates as a binary file
"""
import pickle
import pandas as pd
from datetime import time
from modules.utils import grouper_UT, saveUTdata, list2dict
import os

UT_interval = time(22, 0, 0), time(11, 0, 0)

# first we open the files
file1 = pd.read_csv('./files2cross_corr/file1.csv')
file2 = pd.read_csv('./files2cross_corr/file2.csv')

# now we make sure that the column 'datetime' is indeed datetime
file1['datetime'] = pd.to_datetime(file1['datetime'])
file2['datetime'] = pd.to_datetime(file2['datetime'])


# we have the files ready, now we need to make the UT versions
file1.set_index('datetime', inplace=True)
file2.set_index('datetime', inplace=True)
file1_UT = grouper_UT(file1, *UT_interval)
file2_UT = grouper_UT(file2, *UT_interval)

# we now transform that to dictionaries
file1_UT = list2dict(file1_UT)
file2_UT = list2dict(file2_UT)

# now we save the ut data in the corresponding folders
print('saving file1 nights')
saveUTdata(file1_UT, './UT_data/file1/')
print('saving file2 nights')
saveUTdata(file2_UT, './UT_data/file2/')


# we get the lists of all the generated files
list_of_files_from_file1 = os.listdir('./UT_data/file1/')
list_of_files_from_file2 = os.listdir('./UT_data/file2/')
list_of_files_from_file1.sort()
list_of_files_from_file2.sort()


# now we get the list of the names of the files
list_of_files_from_file1 = [i[: -4] for i in list_of_files_from_file1 if ('.csv' in i)]
list_of_files_from_file2 = [i[: -4] for i in list_of_files_from_file2 if ('.csv' in i)]

# we do a list of the nights that the two sites share
intersected_days = list(set(list_of_files_from_file1) & set(list_of_files_from_file2))

# we now save the list of the shared nights
with open('./UT_data/listofdates.list', 'wb') as f:
    pickle.dump(intersected_days, f)
f.close()
