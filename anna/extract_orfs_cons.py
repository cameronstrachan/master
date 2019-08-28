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

genes_df = pd.read_csv('dataflow/04-analysis-tables/selected_genomes_rbh.csv', low_memory=False)
genes_df_above70 = genes_df.loc[(genes_df['mean_pi'] >= 70)]
genes = genes_df_above70['qseqid'].tolist()

file_obj = sc.Fasta('nitrospinae_genomes.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('nitrospinae_genomes_above70.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.subsetfasta(seqlist = genes, headertag='above70')

genes_df = pd.read_csv('dataflow/04-analysis-tables/selected_genomes_rbh.csv', low_memory=False)
genes_df_above70 = genes_df.loc[(genes_df['mean_pi'] >= 80)]
genes = genes_df_above70['qseqid'].tolist()

file_obj = sc.Fasta('nitrospinae_genomes.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('nitrospinae_genomes_above80.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.subsetfasta(seqlist = genes, headertag='above80')
