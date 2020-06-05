# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/ar/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/ar/')

from modules import seq_core as sc

df_ac_nt_selected = pd.read_csv('dataflow/04-tables/aminoglycoside_nucleotidyltransferases.csv', low_memory=False)


input_dir_genes  = 'dataflow/03-selected-genes/'
input_dir_prots = 'dataflow/03-selected-prots/'

output_dir_genes = 'dataflow/03-selected-genes/aminoglycoside_nucleotidyltransferases/'
output_dir_prots = 'dataflow/03-selected-prots/aminoglycoside_nucleotidyltransferases/'

df_ac_nt_selected = pd.read_csv('dataflow/04-tables/aminoglycoside_nucleotidyltransferases.csv', low_memory=False)
files = list(set(df_ac_nt_selected['query_id'].tolist()))

for file in files:

    file = orf + '.fasta'

    command = 'cp ' + input_dir_genes + file + ' ' + output_dir_genes
    os.system(command)

    command = 'cp ' + input_dir_prots + file + ' ' + output_dir_prots
    os.system(command)
