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

df_representative_genomes = pd.read_csv('dataflow/00-meta/representative_genomes.csv', low_memory=False)
genomes = df_representative_genomes['user_genome'].tolist()
files = [item + ".fna" for item in genomes]

#for file in files:
#    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
#    outputfilename = file.split(".f")[0] + '.faa'
#    file_obj.setOutputName(outputfilename)
#    file_obj.setOutputLocation('dataflow/01-prot/')
#    file_obj.runprodigal()

files = [item + ".faa" for item in genomes]

#for file in files:
#    file_obj = sc.Fasta(file, 'dataflow/01-prot/')
#    file_obj.setOutputName(file)
#    file_obj.setOutputLocation('dataflow/02-blastdbs/')
#    file_obj.runmakeblastdb(dbtype='prot')

file = 'cnoahi_unicycler_closed.faa'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/02-blastdbs/')
file_obj.runmakeblastdb(dbtype='prot')

blastdbs = files.copy()


file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputLocation('dataflow/03-blastout/')
for blastdb in blastdbs:
	outputfilename = file.split('.f')[0] + ':' + blastdb.split('.f')[0] + '.txt'
	file_obj.setOutputName(outputfilename)
	file_obj.runblast(blast='blastp', db=blastdb, dblocation='dataflow/02-blastdbs/', max_target_seqs=1, evalue=1e-3, num_threads = 60)

blastdb = 'cnoahi_unicycler_closed.faa'

for file in files:
	file_obj = sc.Fasta(file, 'dataflow/01-prot/')
	file_obj.setOutputLocation('dataflow/03-blastout/')
	outputfilename = file.split('.f')[0] + ':' + blastdb.split('.f')[0] + '.txt'
	file_obj.setOutputName(outputfilename)
	file_obj.runblast(blast='blastp', db=blastdb, dblocation='dataflow/02-blastdbs/', max_target_seqs=1, evalue=1e-3, num_threads = 60)
