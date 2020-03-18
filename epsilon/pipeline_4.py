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

meta = pd.read_csv('dataflow/00-meta/complete_genomes.csv', low_memory=False)
genomes = meta['File'].tolist()

files = [item + "_genomic.fna" for item in genomes]

for file in files:
    file_path = 'dataflow/01-nucl/complete_genomes/' + file
    
