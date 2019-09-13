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

file_obj = sc.Fasta('nitrospinae_genomes_above80.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('nitrospinae_genomes_above80.fasta')
file_obj.setOutputLocation('dataflow/02-blast/')
file_obj.runonlineblast(blasttype='blastp', database="nr", numhits=10, evalue=0.005)
