from datetime import timedelta, datetime
import numpy as np
import pandas as pd
import os
import pickle
from numpy import polyfit
from astropy.time import Time


def get_mean_diff_from_df(path_2_df):
    """
    This function gets the mean difference between samples for a single
    df given the path of the df
    :param path_2_df: path for the df
    :return: mean value for the period of sampling
    """
    df = pd.read_csv(path_2_df, header=None)
    df.columns = ['datetime', 'seeing']
    mean = df.diff().mean()['datetime']
    return mean


def get_min_and_max_mean(df1_path, df2_path):
    """
    This funciton compares the mean sampling rate od two dfs paths
    :param df1: path for df1
    :param df2: path for df2
    :return: (min, max) mean diff between the two paths
    """
    mean1, mean2 = get_mean_diff_from_df(df1_path), get_mean_diff_from_df(df2_path)
    return np.min([mean1, mean2]), np.max([mean1, mean2])




def saveUTdata(dict_of_dfs, directory2save):
    """
    this function saves every df in a dict to a single csv file
    :param dict_of_dfs: dictionary with the various dfs
    :param directory2save: path od the main folder where to save
    :return: None
    """
    dates = [date for date in dict_of_dfs]
    n_dates = len(dates)
    for i, date in enumerate(dates):
        if i % 200 == 0:
            print(i + 1, '/', n_dates)
        df = dict_of_dfs[date]
        df.index = Time(df.index).to_value('jd')
        df.reset_index(level=0, inplace=True)

        where2save = directory2save + date + '.csv'

        tosave = df.dropna().values
        if len(tosave) > 10:
            np.savetxt(where2save, tosave, delimiter=',')
    return



def grouper_UT(df, UTb, UTe):
    '''
    df: df to slice (must be sorted by date)
    UTb: begining UT time of interest
    UTe: end of UT time of interest (next day)

    return: a list of dfs with the slices
    '''
    n_days = (df.index[-1] - df.index[0]).days

    date_0 = df.index.date[0]
    date_f = date_0 + timedelta(days=1)

    date_0 = datetime.combine(date_0, UTb)
    date_f = datetime.combine(date_f, UTe)

    condition = (date_0 < df.index) & (df.index < date_f)
    conditions = [condition]
    conditions += [((date_0 + timedelta(days=i)) < df.index) & (
                df.index < (date_f + timedelta(days=i)))
                   for i in range(n_days)]

    UT_days = [df.loc[single_condition] for single_condition in conditions][1:]  # the first item is repeated


    return UT_days


def list2dict(list_dfs):
    """
    it takes a list of sliced dfs and turns it into a dict with
    the date as key
    :param list_dfs: a list of ut sampled dfs
    :return: a dict of ut sampled dfs
    """

    return {df.index[0].strftime('%Y-%m-%d'): df for df in list_dfs
            if len(df) != 0}


def resample_df(dict_df, T):

    """
    this function resamples a dict of df to the desired sampling rate
    and returns a dict identical but with the new sampling rate
    :param dict_df: dictionary of dfs to resample
    :param T: sampling rate as str (example: '5Min')
    :return: a dictionary of dataframes with the new sampling rate
    """
    return {date: dict_df[date].resample(T).mean()
            for date in dict_df}





def get_polinomial_parameters(dict_df, degree):
    """
    This function gets a polynomial fit for a dict of utdfs
    :param dict_df: utdf dict
    :param degree: degree of the polynomial desired
    :return: dict of dicts with the parameters consulted with sub keys
    """

    parameters_dict = {}

    for date in dict_df:
        if len(dict_df[date].dropna()) != 0:
            df1 = dict_df[date].paranal.dropna()
            df2 = dict_df[date].armazones.dropna()
            index_1_0 = df1.index[0]
            index_2_0 = df2.index[0]
            p1 = polyfit((df1.index-index_1_0).total_seconds(), df1.values, degree)
            p2 = polyfit((df2.index-index_2_0).total_seconds(), df2.values, degree)
            sub_dict = {'paranal_parameters': p1,
                        'armazones_parameters': p2}
            parameters_dict[date] = sub_dict

    return parameters_dict




def get_resampled_data_merged_df(data_path):
    """
    creates a dataframe of all resampled data from a path
    :param data_path: folder where the data is
    :return: pandas df
    """
    print('getting resampled_raw_data')
    resampled_data_paths = os.listdir(data_path)

    resampled_data_dfs = []

    # for each name of file
    for resampling_rate in resampled_data_paths:
        # open it
        print('opening ' + data_path + resampling_rate)
        with open(data_path + resampling_rate, 'rb') as f:
            current_resampled_data = pickle.load(f)
        f.close()

        # see all the dates present in the current dict
        for date in current_resampled_data:

            df = current_resampled_data[date]

            new_df = pd.DataFrame({'date_key': date,
                                   'datetime': df.index,
                                   'sampling_rate': int(resampling_rate[:-13]),
                                   'paranal_raw': df.paranal.values,
                                   'armazones_raw': df.armazones.values
                                   })

            resampled_data_dfs.append(new_df)

    print('merging the data, this may take a while...')
    print('\n\n\n\n\n')
    # dataframe for the resampled data
    return pd.concat(resampled_data_dfs).sort_values(['sampling_rate', 'datetime'])







def get_mean_norm_data_merged_df(data_path):
    """
    creates a dataframe of all resampled data from a path
    :param data_path: folder where the data is
    :return: pandas df
    """
    print('getting mean_norm_data')
    mean_norma_paths = os.listdir(data_path)

    mean_norm_dfs = []

    # for each name of file
    for resampling_rate in mean_norma_paths:
        # open it
        print('opening ' + data_path + resampling_rate)
        with open(data_path + resampling_rate, 'rb') as f:
            current_mean_norm_data = pickle.load(f)
        f.close()

        # see all the dates present in the current dict
        for date in current_mean_norm_data:

            df = current_mean_norm_data[date]

            new_df = pd.DataFrame({'date_key': date,
                                   'datetime': df.index,
                                   'sampling_rate': resampling_rate[:-13],
                                   'paranal_mean_norm': df.paranal.values,
                                   'armazones_mean_norm': df.armazones.values
                                   })

            mean_norm_dfs.append(new_df)

    print('merging the data, this may take a while...')
    print('\n\n\n\n\n')
    # dataframe for the resampled data
    return pd.concat(mean_norm_dfs).sort_values('datetime').sort_values(['sampling_rate', 'datetime'])




def add_date_key_to_dfs_of_dictionary(dict_of_dfs):
    """
    this function takes a dictionary that contains many resampled days
    and puts a date_key into them to retun a whole df
    :param dict_of_dfs: a dictionary of dfs (have to open bin first)
    :return: a dictionary with the nwe column
    """
    keys = [i for i in dict_of_dfs]
    for key in keys:
        dict_of_dfs[key].loc[:, 'date_key'] = dict_of_dfs[key].index[0].strftime('%Y-%m-%d')
        dict_of_dfs[key].reset_index(level=0, inplace=True)

    return dict_of_dfs

def mean_norm(df):
    #return df/df.mean()
    return (df - df.mean()) / df.std()

def mean_norm_current_df(df):
    df.loc[:, ('paranal_mean_norm')] = mean_norm(df['paranal'])
    df.loc[:, ('armazones_mean_norm')] = mean_norm(df['armazones'])



def mean_normalize(dict_df):
    """
    This function get the paranal data and armazones data and ads two
    mean normalized columns for the dfs in the dict, one for each site
    :param df: dataframe with all the paranal and armazones data
    :return: dict of dfs with two new columns
    """


    keys = [key for key in dict_df]
    n_keys = str(len(keys))
    for i, key in enumerate(keys):
        if i % 100 == 0:
            print('mean normalizing day ' + str(i) + '/' + n_keys)
        current_df = dict_df[key]
        mean_norm_current_df(current_df)
    return dict_df


def divider4corr(length):
    a = np.arange(1, length, 1)
    b = np.arange(length, 0, -1)
    return np.concatenate((a,b))



def make_df_from_dict(dict_dfs):
    """
    This functions takes a dict of dfs and merges it into a big one
    :param dict_dfs: dictionary with the dfs
    :return: big dictionary
    """
    keys = [key for key in dict_dfs]

    dfs_to_append = []

    for key in keys:
        dfs_to_append.append(dict_dfs[key])

    return pd.concat(dfs_to_append)


def get_max_corr_from_df(df):
    """
    This function takes the max corr values for a df of correlations,
    separing mean_norm of non_mean_norm (without prefix)
    :param df: df of correlations
    :return: df max_corr
    """
    max_cross_corr = df[df['cross_corr'] == df['cross_corr'].max()][['shift', 'cross_corr']]
    max_cross_corr_mean_norm = df[df['cross_corr_mean_norm'] == df['cross_corr_mean_norm'].max()][['shift_mean_norm', 'cross_corr_mean_norm']]
    df_4_return = pd.DataFrame(pd.concat([max_cross_corr, max_cross_corr_mean_norm], sort=True).sum()).T

    return df_4_return



def get_max_corr_from_dict(dict_df):
    """
    This function generates a big dataframe with the max correlations
    from a dict of dataframes
    :param dict_df: dict of dataframes with the date_key as keys and the
    correlation data.
    :return: dataframe of max_corr data for the sampling rate used
    """

    keys = [key for key in dict_df]
    df_4_concat = []
    for key in keys:
        current_df = get_max_corr_from_df(dict_df[key])
        current_df.loc[:, ('date_key')] = key
        df_4_concat.append(current_df)
    return pd.concat(df_4_concat)


def shift_to_actual_minutes(dict_w_date_key, sampling_rate):
    """
    This file makes shure the shift for the corr data is in minutes
    :param dict_w_date_key: dictionary of one sampling rate
    :param sampling_rate: sampling rate of the dict
    :return: the same dict but the shifts ar in minutes
    """
    for date in dict_w_date_key:
        dict_w_date_key[date]['shift'] *= sampling_rate
        dict_w_date_key[date]['shift_mean_norm'] *= sampling_rate
    return dict_w_date_key


def shift(array, shift_value):
    """
    This function implements the shift of a timeseries according to the
    maxshift

    Important: Note thet th df with the max_corr has the shifts in
    minutes, hence one have to divide by the sampling rate and convert
    to int prior to using this function
    :param array: array wanted to be shifted
    :param shift_value: the amount of the shift in index units
    :return: returns a shifted array with nans where the tail of the
    shift is
    """
    assert (type(shift_value) == int)

    lenght = len(array)
    out = np.zeros(lenght)

    if shift_value < 0:
        shifted_non_nan = array[-shift_value:]
        out[: shift_value] = shifted_non_nan
        out[shift_value:] = np.nan
    elif shift_value == 0:
        return array
    else:
        shifted_non_nan = array[: -shift_value]
        out[shift_value:] = shifted_non_nan
        out[:shift_value] = np.nan
    return out




def calc_diff_shifted(df):
    """
    computes the subtraction between two datasets and sum
    :param df: df to compute
    :return: sum of the subtraction
    """
    df = df.dropna()
    cols = df.columns
    subtraction_norm = np.abs(df[cols[0]] - df[cols[1]])
    return (subtraction_norm.values/len(df)).sum()



def get_date_key_from_cross_corr_file(file_name):
    return file_name[-14:-4]
