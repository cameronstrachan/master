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

genomes_df = pd.read_csv('dataflow/00-meta/stewart2019_epsilonproteobacteria.csv', low_memory=False)
genomes = genomes_df['file_unzip'].tolist()

# these are the directories we are working with
indir = 'dataflow/01-prot/'
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

for genome in genomes:

    file = genome

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/01-prot/')
    file_obj.runprodigal()


    file_obj = sc.Fasta(file, indir)
    file_obj.setOutputName(file)
    file_obj.setOutputLocation(blastdbdir)
    file_obj.runmakeblastdb(dbtype='prot')



for genome in genomes:
    # blast database names
    blastdbs = genomes.copy()

    # blast all files against all blast databases (all against all)
    for genome in genomes:
        file = genome
        file_obj = sc.Fasta(file, indir)
        file_obj.setOutputLocation(blastdir)
        for blastdb in blastdbs:
            outputfilename = file.split('.f')[0] + '.' + blastdb.split('.f')[0] + '.txt'
            file_obj.setOutputName(outputfilename)
            file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-3, num_threads = 4)
