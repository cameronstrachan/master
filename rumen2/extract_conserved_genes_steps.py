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

blastdb = 'dataflow/02-blast-db/'
blastout = 'dataflow/02-blast-out/'
blastxml = 'dataflow/02-blast-xml/'
blastin = 'dataflow/01-nucl/'
prot_dir = 'dataflow/01-prot/'
analysis_folder = 'dataflow/03-analysis/'
dbs = ['campylobacter_coli.fasta', 'listeria_monocytogenes.fasta', 'staphylococcus_aureus.fasta', 'pseudomonas_aeruginosa.fasta', 'campylobacter_jejuni.fasta', 'clostridioides_difficile.fasta', 'acinetobacter_baumannii.fasta', 'streptococcus_pneumoniae.fasta', 'neisseria_gonorrhoeae.fasta']
output_files_blast = []

file_obj = sc.Fasta(input_file, blastin)
file_obj.setOutputName(input_file)
headers = file_obj.fasta2headermap()

analysis_folder = 'dataflow/03-analysis/'
df = pd.DataFrame.from_dict(headers, orient="index")
df['file'] = input_file

df.index.name = 'id'
df.reset_index(inplace=True)

df.columns = ['id', 'full_header', 'file']

df['id_unnumbered'] = 'NA'

df['id_unnumbered'] = df.apply(lambda x: str(x['id']).rsplit('_', 1)[0], axis=1)

df = df[df['id'].isin(genes_unique)]

df.to_csv(analysis_folder + input_file.split('.fa')[0] + '_mapped_headers.csv')
