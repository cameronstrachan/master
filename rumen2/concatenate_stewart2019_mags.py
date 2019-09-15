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
df_mags = df[df['type'] == 'MAG']
#files = df_mags['file'].tolist()

#for file in files:
#    command = 'mv dataflow/01-nucl/' + file + ' dataflow/01-nucl/mags/' + file
#    os.system(command)

#os.system('gunzip dataflow/01-nucl/mags/*.gz')

files = df_mags['file_unzip'].tolist()
files_rename = []

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-nucl/mags/')
    outname = file.split('.fa')[0] + '_rename.fasta'
    files_rename.append(outname)
    file_obj.setOutputName(outname)
    file_obj.setOutputLocation('dataflow/01-nucl/mags/')
    #file_obj.headerrename()

sg.concat(inputfolder='dataflow/01-nucl/mags/', outputpath='dataflow/01-nucl/stewart2019_mags.fasta', filenames=files_rename)
