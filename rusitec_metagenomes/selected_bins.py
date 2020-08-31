import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')


df_selected_bins = pd.read_csv('dataflow/00-meta/checkM_select_90_10.csv', low_memory=False)
bins = df_selected_bins['bin'].tolist()

files = [item + ".fa" for item in bins]

for file in files:
    command = 'cp dataflow/04-bins/' + file + ' dataflow/04-bins/selected/'
    os.system(command)