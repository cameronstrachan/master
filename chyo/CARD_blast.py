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


file_obj = sc.Fasta('card_db.fasta', 'fasta/')
file_obj.setOutputName('card_db.fasta')
file_obj.setOutputLocation('blastdb/')
file_obj.runmakeblastdb(dbtype='prot')

file_obj = sc.Fasta('chyo_transcriptome_concensus_genome_prot_trimmed_100.fasta', 'fasta/')
file_obj.setOutputLocation('blast_output/')
file_obj.setOutputName('CARD_blast.txt')
file_obj.runblast(blast='blastp', db='card_db.fasta', dblocation='blastdb/', max_target_seqs=1, evalue=1e-5, num_threads = 30)
