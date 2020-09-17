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

#files = [f for f in os.listdir('dataflow/01-nucl/') if f.endswith(".fasta")]

#for file in files:
#   file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
#   outputfilename = file.split(".f")[0] + '.faa'
#   file_obj.setOutputName(outputfilename)
#   file_obj.setOutputLocation('dataflow/01-prot/')
#   file_obj.runprodigal()

files = [f for f in os.listdir('dataflow/01-prot/') if f.endswith(".faa")]

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-prot/')
    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/02-blastdbs/')
    file_obj.runmakeblastdb(dbtype='prot')

blastdbs = files.copy()

for file in files:

    blastdbs = files.copy()
    file_obj = sc.Fasta(file, 'dataflow/01-prot/')
    file_obj.setOutputLocation('dataflow/03-blastout/')
    for blastdb in blastdbs:
    	outputfilename = file.split('.f')[0] + ':' + blastdb.split('.f')[0] + '.txt'
    	file_obj.setOutputName(outputfilename)
    	file_obj.runblast(blast='blastp', db=blastdb, dblocation='dataflow/02-blastdbs/', max_target_seqs=1, evalue=1e-3, num_threads = 60)
