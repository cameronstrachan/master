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


input_dir_genes  = 'dataflow/02-genes/'
input_dir_prots = 'dataflow/02-prots/'

output_dir_genes_aph = 'dataflow/03-selected-genes/aminoglycoside_modifying/phosphotransferases/'
output_dir_prots_aph = 'dataflow/03-selected-prots/aminoglycoside_modifying/phosphotransferases/'

output_dir_genes_ant = 'dataflow/03-selected-genes/aminoglycoside_modifying/nucleotidyltransferases/'
output_dir_prots_ant = 'dataflow/03-selected-prots/aminoglycoside_modifying/nucleotidyltransferases/'

# aminoglycoside phosphotransferases

df_ac_nt_selected_phosphotransferase = pd.read_csv('dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying_aph.csv', low_memory=False)

for index, row in df_ac_nt_selected_phosphotransferase.iterrows():

    orf = row['query_id']
    file = row['file']

    file_obj = sc.Fasta(file, input_dir_genes)
    file_obj.setOutputName(orf + '.fasta')
    file_obj.setOutputLocation(output_dir_genes_aph)
    file_obj.subsetfasta(seqlist = [orf])

    file_obj = sc.Fasta(file, input_dir_prots)
    file_obj.setOutputName(orf + '.fasta')
    file_obj.setOutputLocation(output_dir_prots_aph)
    file_obj.subsetfasta(seqlist = [orf])


# aminoglycoside nucleotidyltransferases

df_ac_nt_selected_nucleotidyltransferase = pd.read_csv('dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying_ant.csv', low_memory=False)

for index, row in df_ac_nt_selected_phosphotransferase.iterrows():

    orf = row['query_id']
    file = row['file']

    file_obj = sc.Fasta(file, input_dir_genes)
    file_obj.setOutputName(orf + '.fasta')
    file_obj.setOutputLocation(output_dir_genes_ant)
    file_obj.subsetfasta(seqlist = [orf])

    file_obj = sc.Fasta(file, input_dir_prots)
    file_obj.setOutputName(orf + '.fasta')
    file_obj.setOutputLocation(output_dir_prots_ant)
    file_obj.subsetfasta(seqlist = [orf])
