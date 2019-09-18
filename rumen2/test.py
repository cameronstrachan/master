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

genes = []
analysis_folder = 'dataflow_test/03-analysis/'
for file in output_files_freq:
    csv_file = analysis_folder + file
    df = pd.read_csv(csv_file, low_memory=False)
    gene_ids = df['gene'].tolist()
    genes = genes + gene_ids

genes_unique = list(set(genes))

blastin = 'dataflow_test/01-nucl/'
input_file = 'stewart2019_mags_genes_sub.fasta'

file_obj = sc.Fasta(input_file, blastin)
file_obj.setOutputName(input_file)
headers = file_obj.fasta2headermap()

headerfile = 'dataflow_test/03-analysis/'
df = pd.DataFrame.from_dict(headers, orient="index")
df['file'] = input_file
#df[df['A'].isin(genes_unique]
df.to_csv(headerfile + input_file.split('.fa')[0] + '.csv')
