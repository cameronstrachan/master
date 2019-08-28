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

blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'
file = 'dna-sequences-99.fasta'

file_obj = sc.Fasta(file, 'dataflow/03-asv-seqs/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = file

file = '16s_Nitrospinae_mapping.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = '16s_Nitrospinae_mapping.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=5, evalue=1e-3, num_threads = 6)
