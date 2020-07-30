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

files = ["Campylobacter_jejuni_ATCC 700819.faa", "Campylobacter_hyointestinalis.faa", "Campylobacter_gracilis.faa", "Campylobacter_concisus.faa"]

for file in files:
    file_obj = sc.Fasta(file, 'assembled_genomes/reference_genomes/')
    file_obj.setOutputName(file)
    file_obj.setOutputLocation('assembled_genomes/blastdbs/')
    file_obj.runmakeblastdb(dbtype='prot')

blastdbs = files.copy()

file_obj = sc.Fasta('spades_coassembly_scaffolds.faa', 'assembled_genomes/spades_coassembly_scaffolds_annotations/')
file_obj.setOutputLocation('dataflow/reference_annotations/')
for blastdb in blastdbs:
	outputfilename = file.split('.f')[0] + ':' + blastdb.split('.f')[0] + '.txt'
	file_obj.setOutputName(outputfilename)
	file_obj.runblast(blast='blastp', db=blastdb, dblocation='blastdbs/', max_target_seqs=1, evalue=1e-3, num_threads = 10)
