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

prots_input_folder = 'dataflow/02-prots/'
genome_extension = '.fasta'

df_CARD_hits = pd.read_csv('dataflow/04-tables/CARD_hits_95_90.csv', low_memory=False)
selected_rumen_genomes = df_CARD_hits['file'].tolist()

header_dfs = []

for file in selected_rumen_genomes:

    file_obj = sc.Fasta(file, prots_input_folder)
    headers = file_obj.fasta2headermap()
    df_headers = pd.DataFrame.from_dict(headers, orient="index")
    df_headers['file'] = file
    header_dfs.append(df_headers)

# clean up header to have start, end and direction of the ORFs
df_final = pd.concat(header_dfs)
df_final.columns = ['header', 'file']
df_positions = df_final['header'].str.split('#', expand=True).loc[:,[1,2,3]]
df_final = pd.concat([df_final, df_positions], axis=1)
df_final = df_final.drop('header', 1)
df_final.columns = ['file', 'start', 'end', 'direction']
df_final['start'] = df_final['start'].str.strip()
df_final['end'] = df_final['end'].str.strip()
df_final['direction'] = df_final['direction'].str.strip()

df_final.to_csv('dataflow/04-tables/rumen_genomes_header_map.csv')
