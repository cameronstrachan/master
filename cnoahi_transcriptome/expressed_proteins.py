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

seq_obj = sc.Fasta('error_corrected_full_genome_prot.fasta', 'error_corrected/')
seq_dic = seq_obj.fasta2dict()

seq_dic_trim = dict(seq_dic)

for k,v in seq_dic.items():
    if 'NN' in v:
        del seq_dic_trim[k]

outputfile = open('error_corrected//error_corrected_full_genome_prot_200.fasta', 'w')

for k,v in seq_dic_trim.items():
    seq = v.rstrip()
    if len(seq) > 200:
        outputfile.write(">" + k + '\n')
        outputfile.write(v + '\n')
