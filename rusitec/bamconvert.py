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

# sort bam files by read name, so that fastq files have the same order
bam_dir = 'dataflow/01-bam/'
bam_files = [f for f in os.listdir(bam_dir) if f.endswith(".bam")]

for bam in bam_files:
    prefix = bam.split('.bam')[0]
    sort_in = bam_dir + bam
    sort_out = bam_dir + prefix + '.sort.bam'
    command = 'samtools sort -n' + ' ' + sort_in + ' ' + '-o' + ' ' + sort_out
    os.system(command)

# convert sorted bam files to fastqs

bam_files_sorted = [f for f in os.listdir('dataflow/01-bam/') if f.endswith(".sort.bam")]
fastq_dir = 'dataflow/01-fastq/'
count = 1

for bam in bam_files_sorted:
    prefix = bam.split('.sort')[0]
    convert_in = bam_dir + bam
    sample_id = prefix.split('#')[1].split('_')[0]
    convert_out_pair1 = fastq_dir + sample_id + '_' + 'S' + str(count) + '_L001_R1_001.fastq'
    convert_out_pair2 = fastq_dir + sample_id + '_' + 'S' + str(count) + '_L001_R2_001.fastq'
    command = 'bedtools bamtofastq -i' + ' ' + convert_in + ' -fq ' + convert_out_pair1 + ' -fq2 ' + convert_out_pair2
    os.system(command)
