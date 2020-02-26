import pandas as pd
import pickle

with open('UT_data/listofdates.list', 'rb') as f:
    date_keys = pickle.load(f)
f.close()

ns = []


for date in date_keys:
    file1_current = pd.read_csv('./UT_data/file1/'+date+'.csv', header=None)
    file2_current = pd.read_csv('./UT_data/file2/' + date + '.csv', header=None)
    n = len(file1_current) + len(file2_current)
    ns.append(n)

df = pd.DataFrame({'date_key': date_keys, 'n_points': ns})

with open('n_points/n_points.df', 'wb') as f:
    pickle.dump(df, f)
f.close()
