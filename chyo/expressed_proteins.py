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

seq_obj = sc.Fasta('chyo_transcriptome_concensus_genome_nucl.fasta', 'expressed/')
seq_dic = seq_obj.fasta2dict()

seq_dic_trim = dict(seq_dic)

for k,v in seq_dic.items():
    if 'NN' in v:
        del seq_dic_trim[k]

outputfile = open('expressed/chyo_transcriptome_concensus_genome_nucl_trimmed_100.fasta', 'w')

for k,v in seq_dic_trim.items():
    seq = v.rstrip()
    if len(seq) > 100:
        outputfile.write(">" + k + '\n')
        outputfile.write(v + '\n')
