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

file_obj = sc.Fasta('metagenome_genes.fasta', blastin)
file_obj.setOutputName('metagenome_genes_campylobacter_coli.txt')
file_obj.setOutputName(blastout)
file_obj.runblast(blast='blastn', db=blastdb, dblocation='campylobacter_coli.fasta', max_target_seqs=5000, evalue=1e-3, num_threads = 60, max_hsps = 1)
