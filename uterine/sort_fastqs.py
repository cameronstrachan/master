# ENV anaconda
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
from modules import seq_scrape as ss

ss.srafastqdownlaod('SRX848536', outputdir='dataflow/01-fastq/')

fq_dir = 'dataflow/01-fastq/'
fq_files = [f for f in os.listdir(fq_dir) if f.endswith(".fastq.gz")]
count = 1

for fq in fq_files:
    prefix = fq.split('.fastq.gz')[0]
    acc = prefix.split('_')[0]
    pair = prefix.split('_')[2]

    if pair == '1':
        input = fq_dir + fq
        output = fq_dir + 'forward/' + acc + '_' + 'S' + str(count) + '_L001_R1_001.fastq'
        command = 'cp ' + input + ' ' + output
        os.system(command)

    count = count + 1
