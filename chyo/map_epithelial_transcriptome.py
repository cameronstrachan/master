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

#bwa index cyo1_nanopore.fasta

files = [f for f in os.listdir('.') if f.endswith(".fastq")]

for file in files:
    file_prefix = file.split('_')[0] + "_" + file.split('.')[1]
    sam_file = file_prefix + ".sam"
    command = "bwa mem -t 60 -B 1 -k 8 -O 2 cyo1_nanopore.fasta " + file + " > " + sam_file
    os.system(command)

    bam_file = file_prefix + ".bam"
    command = "samtools view -@ 60 -bS " + sam_file + " > " + bam_file
    os.system(command)

    bam_file_sorted = file_prefix + ".sorted.bam"
    command = "samtools sort -@ 60 " + sam_file + " > " + bam_file_sorted
    os.system(command)
