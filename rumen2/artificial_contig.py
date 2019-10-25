import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta("campylobacter_coli_cluster_assembly_100.fasta", 'dataflow/01-nucl/')
file_obj.setOutputName("campylobacter_coli_cluster_assembly_100.fasta")
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.runprodigal()

# annotate genes against CARD
db_file = "card_db.fasta"
blastdb = 'dataflow/02-blast-db/'
blastout = 'dataflow/02-blast-out/'

file_obj = sc.Fasta("campylobacter_coli_cluster_assembly_100.fasta", 'dataflow/01-prot/')
file_obj.setOutputLocation(blastout)
outputfilename = "campylobacter_coli_cluster_assembly_100" + '_card.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastp', db=db_file, dblocation=blastdb, max_target_seqs=1, evalue=1e-3, num_threads = 60)
