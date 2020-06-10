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


input_dir_genes  = 'dataflow/03-genes/'
input_dir_prots = 'dataflow/03-prots/'

output_dir_genes = 'dataflow/03-selected-genes/aminoglycoside_modifying/'
output_dir_prots = 'dataflow/03-selected-prots/aminoglycoside_modifying/'


# aminoglycoside phosphotransferases

df_ac_nt_selected_phosphotransferase = pd.read_csv('dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying_aph.csv', low_memory=False)
files1 = list(set(df_ac_nt_selected_phosphotransferase['query_id'].tolist()))

for file in files1:

    file_w_ext = file + '.fasta'

    command = 'cp ' + input_dir_genes + file_w_ext + ' ' + output_dir_genes + 'phosphotransferases/'
    os.system(command)

    command = 'cp ' + input_dir_prots + file_w_ext + ' ' + output_dir_prots + 'phosphotransferases/'
    os.system(command)

# aminoglycoside nucleotidyltransferases

df_ac_nt_selected_nucleotidyltransferase = pd.read_csv('dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying_ant.csv', low_memory=False)
files2 = list(set(df_ac_nt_selected_nucleotidyltransferase['query_id'].tolist()))

for file in files2:

    file_w_ext = file + '.fasta'

    command = 'cp ' + input_dir_genes + file_w_ext + ' ' + output_dir_genes + 'nucleotidyltransferases/'
    os.system(command)

    command = 'cp ' + input_dir_prots + file_w_ext + ' ' + output_dir_prots + 'nucleotidyltransferases/'
    os.system(command)
