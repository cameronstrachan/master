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

file_obj = sc.Fasta('neubauer2018_wetzels201_99.fasta', 'dataflow/03-asv-seqs/')
file_obj.setOutputName('neubauer2018_wetzels201_99_oneline.fasta')
file_obj.setOutputLocation('dataflow/03-asv-seqs/')
file_obj.saveonelinefasta(header='none')

df_seqs = pd.read_csv('dataflow/00-meta/core_microbiome_seqs.csv', low_memory=False)
seqs_asvs = df_seqs['asv'].tolist()

file_obj = sc.Fasta('neubauer2018_wetzels201_99_oneline.fasta', 'dataflow/03-asv-seqs/')
file_obj.setOutputName('core_epithelial_microbiome_99_oneline.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.subsetfasta(seqlist = seqs_asvs, headertag='none')
