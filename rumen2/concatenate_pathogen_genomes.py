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

dirs = ['listeria_monocytogenes', 'campylobacter_coli', 'staphylococcus_aureus']
head_dir = 'dataflow/01-nucl/'

for dir in dirs:
    path_dir = head_dir + dir + '/'
    unzip_command = 'gunzip ' + path_dir + '*.gz'
    os.system(unzip_command)
    lis = [f for f in os.listdir(path_dir) if f.endswith(".fna")]
    output_file = head_dir + dir + '.fasta'
    sg.concat(inputfolder=path_dir, outputpath=output_file, filenames=lis)
