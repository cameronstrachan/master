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

files = ['clostridioides_difficile_dave.fasta']

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/02-blast-db/')
    file_obj.runmakeblastdb(dbtype='nucl')
