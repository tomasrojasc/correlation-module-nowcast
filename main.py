import os
os.system('bash prepare_folders.sh')
import scripts.prepare_csv_files
import scripts.making_cross_corr
import scripts.making_df_with_cross_corrs
import scripts.getting_max_corr
os.system('bash clean.sh')
