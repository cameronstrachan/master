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

from modules import seq_scrape as ss
### Environment: source activate anaconda to dowload data


accession_nums = list(range(374, 536, 1))
accession_list = ['SRX848' + str(x) for x in accession_nums]

for acc in accession_list:
    ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/')
