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

genomes_input_folder = 'dataflow/01-genomes/'
genome_extension = '.fasta'

genome_files = [f for f in os.listdir(genomes_input_folder) if f.endswith(genome_extension)]

for file in genome_files:

    file_obj = sc.Fasta(file, 'dataflow/01-genomes/')
    file_obj.setOutputName(file)

    file_obj.setOutputLocation('dataflow/02-prots/')
    file_obj.runprodigal(type = 'prot')

    file_obj.setOutputLocation('dataflow/02-genes/')
    file_obj.runprodigal(type = 'nucl')
