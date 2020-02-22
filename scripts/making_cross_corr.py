"""
This file is the file in charge of doing the cross correlations.

To be able to do this, it uses the cross correlation module pydcf

At the same time, takes each output and it saves it as a csv file
with the lag, the corr and the error
"""


import os
import pickle
from modules.utils import get_min_and_max_mean
from datetime import timedelta
from astropy.time import TimeDelta
from modules.config import delay, bin_width

# delete if the folders do already have files
os.system('find output/ -type f -delete')

# opening the list of dates
with open('UT_data/listofdates.list', 'rb') as f:
    dates = pickle.load(f)
f.close()


# we are interested in delays up to 5 hrs
delay = TimeDelta(timedelta(hours=delay)).to_value('jd')
dates.sort()
n_dates = str(len(dates))
no_plot = '-np --no-plot'
with_out = '-o --output'
spaces = '                                                             '
for i, date in enumerate(dates):
    print(spaces*2+'('+str(i)+'/'+n_dates+')')
    current_file1_path = './UT_data/file1/' + date + '.csv'
    current_file2_path = './UT_data/file2/' + date + '.csv'
    min_sampling_period, max_sampling_period = get_min_and_max_mean(current_file1_path, current_file2_path)
    print('doing corr for date:', date)
    print('bin =', bin_width, 'times max period')
    actual_bin = bin_width * max_sampling_period
    folder_2_output = './output/'
    file_name = 'out'+str(bin_width)+'_'+date+'.csv'
    command = ' '.join(['python3.7 -W ignore ./pydcf/dcf.py', current_file1_path, current_file2_path, str(-delay),  str(delay), str(actual_bin), with_out, no_plot])
    final_path = folder_2_output + file_name
    command4move = 'mv ./dcf_output.csv ' + final_path
    # commands
    os.system(command)
    os.system(command4move)
