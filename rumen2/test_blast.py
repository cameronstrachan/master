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
file_obj.setOutputName('metagenome_genes_300.fasta')
file_obj.setOutputLocation(blastin)
file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'above')

file_obj = sc.Fasta('metagenome_genes_300.fasta', blastin)
file_obj.setOutputName('metagenome_genes_campylobacter_coli.txt')
file_obj.setOutputLocation(blastout)
file_obj.runblast(blast='blastn', db='campylobacter_coli.fasta', dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)

#

file_obj = sc.Fasta('metagenome_genes_300.fasta', blastin)
file_obj.setOutputName('metagenome_genes_listeria_monocytogenes.txt')
file_obj.setOutputLocation(blastout)
file_obj.runblast(blast='blastn', db='listeria_monocytogenes.fasta', dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)

#

file_obj = sc.Fasta('metagenome_genes_300.fasta', blastin)
file_obj.setOutputName('metagenome_genes_staphylococcus_aureus.txt')
file_obj.setOutputLocation(blastout)
file_obj.runblast(blast='blastn', db='staphylococcus_aureus.fasta', dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)
