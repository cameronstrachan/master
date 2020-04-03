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

dir = 'tara/'
file = '16S.OTU.SILVA.reference.sequences.fna'

file_obj = sc.Fasta(file, dir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(dir)
file_obj.runmakeblastdb(dbtype='nucl')


file = 'selected_long_16s.fasta'

file_obj = sc.Fasta(file, dir)
file_obj.setOutputLocation(dir)

db = '16S.OTU.SILVA.reference.sequences.fna'
outputfilename = '16s_tara_rep_seqs.txt'

file_obj.setOutputName(outputfilename)

file_obj.runblast(blast='blastn', db=db, dblocation=dir, max_target_seqs=1, evalue=1e-3, num_threads = 6, max_hsps = 1)
