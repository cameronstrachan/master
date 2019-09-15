# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

df = pd.read_csv('dataflow/00-meta/stewart2019_ftp_meta.csv', low_memory=False)
df_mags = df[df['scientific_name'] == 'MAG']
files = df_mags['file'].tolist()

for file in files:
    command = 'mv dataflow/01-nucl/' + file + ' dataflow/01-nucl/mags/' + file
    print(command)
    #os.system(command)

#os.system('gunzip dataflow/01-nucl/mags/*.gz')

#files = df_mags['file_unzip'].tolist()

#sg.concat(inputfolder='dataflow/01-nucl/mags/', outputpath='dataflow/01-nucl/stewart2019_mags.fasta', filenames=files)
