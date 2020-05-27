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

df_card_selected = pd.read_csv('dataflow/04-tables/CARD_hits_95_90.csv', low_memory=False)

input_dir_genomes = 'dataflow/01-genomes/'
input_dir_genes = 'dataflow/02-genes/'
input_dir_prots = 'dataflow/02-prots/'

output_dir_genomes = 'dataflow/03-selected-genomes/'
output_dir_genes = 'dataflow/03-selected-genes/'
output_dir_prots = 'dataflow/03-selected-prots/'

for index, row in df_card_selected.iterrows():

    orf = row['query_id']
    file = row['file']

    command = 'cp ' + input_dir_genomes + file + ' ' + output_dir_genomes
    os.system(command)

    print(orf)
    print(list(orf))

    file_obj = sc.Fasta(file, input_dir_genes)
    file_obj.setOutputName(orf + '.fasta')
    file_obj.setOutputLocation(output_dir_genes)
    #file_obj.subsetfasta(seqlist = list(orf))

    file_obj = sc.Fasta(file, input_dir_prots)
    file_obj.setOutputName(orf + '.fasta')
    file_obj.setOutputLocation(output_dir_prots)
    #file_obj.subsetfasta(seqlist = list(orf))
