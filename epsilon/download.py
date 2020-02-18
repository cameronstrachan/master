# python libraries
import os, sys
import subprocess
import pandas as pd

df = pd.read_csv('dataflow/00-meta/stewart2019_epsilonproteobacteria.csv', low_memory=False)
ftps = df['data_ftp'].tolist()

for ftp in ftps:
    command = 'wget -P dataflow/01-nucl/ ' + str(ftp)
    os.system(command)

os.system('gunzip dataflow/01-nucl/*')
