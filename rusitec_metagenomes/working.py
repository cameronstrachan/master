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

files = [f for f in os.listdir('dataflow/01-bam/') if f.endswith(".bam")]

for file in files:
    file_id = file.split('_')[1]
    file_prefix = file.split('.bam')[0]
    file_sorted = file_prefix + ".sorted.bam"
    fastq_sorted = file_prefix + ".sorted.fastq"

    command = 'samtools sort --threads 60 -n dataflow/01-bam/' + file + ' -o dataflow/01-bam/' + file_sorted
    os.system(command)

    command = 'bedtools bamtofastq -i dataflow/01-bam/' + file_sorted + ' -fq dataflow/01-fastq/' + file_id + '_R1.fastq' + ' -fq2 dataflow/01-fastq/' + file_id + '_R2.fastq'
    os.system(command)
