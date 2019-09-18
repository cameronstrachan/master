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

blastdb = 'dataflow_test/02-blast-db/'
blastout = 'dataflow_test/02-blast-out/'
blastin = 'dataflow_test/01-nucl/'
input_file = 'stewart2019_mags_genes_sub.fasta'
dbs = ['campylobacter_coli.fasta', 'listeria_monocytogenes.fasta', 'staphylococcus_aureus.fasta']
output_files_blast = []

for db_file in dbs:
    outname = input_file.split('.fa')[0] + '_' + db_file.split('.fa')[0] + '.txt'
    output_files_blast.append(outname)

command = 'Rscript summarize_hit_frequency.R '
output_files_freq = []

for file in output_files_blast:
    command = command + file + ' '
    outname = file.split('.tx')[0] + '.csv'
    output_files_freq.append(outname)

genes = []
analysis_folder = 'dataflow_test/03-analysis/'
for file in output_files_freq:
    csv_file = analysis_folder + file
    df = pd.read_csv(csv_file, low_memory=False)
    gene_ids = df['gene'].tolist()
    genes = genes + gene_ids

genes_unique = list(set(genes))


#

file_obj = sc.Fasta(input_file, blastin)
file_obj.setOutputName(input_file)
headers = file_obj.fasta2headermap()

headerfile = 'dataflow_test/03-analysis/'
df = pd.DataFrame.from_dict(headers, orient="index")
df['file'] = input_file

df.index.name = 'id'
df.reset_index(inplace=True)

df.columns = ['id', 'full_header']
df['id_unnumbered'] = 'NA'



#df['id_unnumbered'] = df.apply(lambda x: str(x['id']).rsplit('_', 1)[0], axis=1)

#df = df[df['id_unnumbered'].isin(genes_unique)]
df.to_csv(headerfile + input_file.split('.fa')[0] + '_headers.csv')
