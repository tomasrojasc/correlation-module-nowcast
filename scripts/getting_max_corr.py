"""
This file takes all the cross correlation and computes all the maximums
with they corresponding delays. At the ent it saves it into a binary
file in the final_output folder
"""
import pandas as pd
import pickle

# opening the data
with open('./final_output/final_df.correlations', 'rb') as f:
    df = pickle.load(f)
f.close()


date_keys = df['date_key'].unique().tolist()
bin_widths = df['bin_width'].unique().tolist()

dfs_4_concat = []
for date_key in date_keys:
    print('working for date', date_key)
    condition1 = df['date_key'] == date_key
    for bin_width in bin_widths:
        condition2 = df['bin_width'] == bin_width

        current_df = df[condition1 & condition2]

        dfs_4_concat.append(current_df[current_df['cross_corr'] == current_df['cross_corr'].max()])

print('merging')
final_df = pd.concat(dfs_4_concat)

with open('final_output/max_corr_df.correlations', 'wb') as f:
    pickle.dump(final_df, f)
f.close()






