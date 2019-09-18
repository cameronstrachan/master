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

file_obj = sc.Fasta('stewart2019_mags_genes_sub_pathogen_mapped.fasta', 'dataflow_test/01-prot/')
file_obj.setOutputLocation('dataflow_test/02-blast-out/')

outputfilename = "stewart2019_mags_genes_sub_pathogen_mapped_card.txt"
db_file = "card_db.fasta"

file_obj.setOutputName(outputfilename)

file_obj.runblast(blast='blastp', db=db_file, dblocation=blastdb, max_target_seqs=10, evalue=1e-3, num_threads = 60)
