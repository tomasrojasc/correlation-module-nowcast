"""
This script takes all the files make by the correlation pydcf and merges
everything into a big dataframe that contains the lag in minutes,
the cross corr, the lag in hours, the err cross corr and the date_key
"""

import pickle
import pandas as pd
import os
from astropy.time import TimeDelta
from modules.utils import get_date_key_from_cross_corr_file
from modules.config import bin_width

folder_name = './output/'

df_list = []

files_in_folder = os.listdir(folder_name)
files_in_folder.sort()
files_in_folder = [i for i in files_in_folder if ('.csv' in i)]
full_paths = [folder_name + i for i in files_in_folder]

for i, path in enumerate(full_paths):
    date_key = get_date_key_from_cross_corr_file(files_in_folder[i])
    df = pd.read_csv(path)
    df['bin_width'] = bin_width
    df['date_key'] = date_key
    df_list.append(df)


print('merging...')
final_df = pd.concat(df_list)

final_df['# LAG'] = pd.to_timedelta(TimeDelta(final_df['# LAG'], format='jd').datetime)
final_df['# LAG'] = final_df['# LAG'].dt.total_seconds()/60
final_df.rename(columns={'# LAG': 'lag_in_minutes', 'DCF': 'cross_corr', 'DCF_ERROR': 'cross_corr_err'}, inplace=True)
final_df['lag_in_hours'] = final_df['lag_in_minutes']/60 


print('saving...')
with open('./final_output/final_df.correlations', 'wb') as f:
    pickle.dump(final_df, f)
f.close()
