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

df_representative_genomes = pd.read_csv('dataflow/00-meta/representative_genomes.csv', low_memory=False)
genomes = df_representative_genomes['user_genome'].tolist()
files = [item + ".fna" for item in genomes]

for file in files:
	command = 'mv dataflow/01-nucl/' + file + ' dataflow/to_move/'
	os.system(command)