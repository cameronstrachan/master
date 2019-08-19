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

actino_seqs = pd.read_csv('actinobacteria_silva_seqs.csv', low_memory=False)
actino_seqs_acc = actino_seqs['accession'].tolist()

file_obj = sc.Fasta('silva_132_99_16S.fna', '00-databases/')
file_obj.setOutputName('actino_bacteria_seqs.fasta')
file_obj.setOutputLocation('01-nucl/')
file_obj.subsetfasta(seqlist = actino_seqs_acc, headertag='actino')
