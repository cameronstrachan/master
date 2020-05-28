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

genomes_input_folder = 'dataflow/03-selected-genomes/'
genome_extension = '.fasta'

genomes_files = [f for f in os.listdir(genomes_input_folder) if f.endswith(genome_extension)]

header_dfs = []

for file in genomes_files:

    file_obj = sc.Fasta(file, genomes_input_folder)
    headers = file_obj.fasta2headermap()
    df_headers = pd.DataFrame.from_dict(headers, orient="index")
    df_headers['file'] = file
    header_dfs.append(df_headers)

df_final = pd.concat(header_dfs)
df_final.to_csv('dataflow/04-tables/rumen_genomes_header_map.csv')
