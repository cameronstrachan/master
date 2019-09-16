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
df_meta = df[df['type'] == 'metagenome']
files = df_meta['file_unzip'].tolist()

files_rename = []

for file in files:
    outname = file.split('.fa')[0] + '_rename.fasta'
    files_rename.append(outname)

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-nucl/metagenomes/')
    file_outname = file.split('.fa')[0] + '_genes.fasta'
    file_obj.setOutputName(file_outname)
    file_obj.setOutputLocation('dataflow/01-nucl/metagenomes/')
    file_obj.runprodigal(type='nucl')
