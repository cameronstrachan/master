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

file_obj = sc.Fasta('campy1_top250_ncbi.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('campy1_top250_ncbi_oneLine.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.saveonelinefasta(header='none')
