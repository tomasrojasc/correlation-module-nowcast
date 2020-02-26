import pickle
import pandas as pd

with open('n_points/n_points.df', 'rb') as f:
    n_points = pickle.load(f)
f.close()

with open('final_output/max_corr_df.correlations', 'rb') as f:
    max_corr_df = pickle.load(f)
f.close()

final_df = pd.merge(max_corr_df, n_points, on='date_key')

with open('final_output/max_corr_df.correlations', 'wb') as f:
    pickle.dump(final_df, f)
f.close()
