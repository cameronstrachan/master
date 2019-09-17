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

met_dir = 'dataflow_test/01-nucl/metagenomes/'

lis = [f for f in os.listdir(met_dir) if f.endswith("_genes.fasta")]
sg.concat(inputfolder=met_dir, outputpath='dataflow_test/01-nucl/metagenome_genes.fasta', filenames=lis)
