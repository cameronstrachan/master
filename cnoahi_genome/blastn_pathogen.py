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

blastdbs = ['staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis']

file = 'cnoahi_unicycler_closed_no_rRNA.ffn'

file_obj = sc.Fasta(file, 'assembled_genomes/cnoahi_unicycler_closed_annotations/')
file_obj.setOutputLocation('assembled_genomes/reference_annotations/pathogen_blast/')

for blastdb in blastdbs:
	outputfilename = file.split('.f')[0] + ':' + blastdb.split('.f')[0] + '.txt'
	file_obj.setOutputName(outputfilename)
	file_obj.runblast(blast='blastn', db=blastdb, dblocation='../ar/dataflow/01-dbs/blastdbs/', max_target_seqs=100, evalue=1e-3, num_threads = 60)
