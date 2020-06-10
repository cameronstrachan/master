# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/ar/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/ar/')

from modules import seq_core as sc

df_selected = pd.read_csv('dataflow/00-meta/selected_genomes.csv', low_memory=False)

for index, row in df_selected.iterrows():
    file = row['file']
    command = cp '../trees/concatenated_marker/complete_genomes/' + file + ' dataflow/dataflow/01-nucl/'

nucl_dir = 'dataflow/01-nucl/'
prot_dir = 'dataflow/01-prot/'

files = [f for f in os.listdir(nucl_dir) if f.endswith(".fna")]

for file in files:

  file_obj = sc.Fasta(file, "dataflow/01-nucl/")

  outfilename = file.split('.f')[0] + '_rename.fna'

  file_obj.setOutputName(outfilename)
  file_obj.setOutputLocation("dataflow/01-nucl/")
  file_obj.headerrename()

files = [f for f in os.listdir(nucl_dir) if f.endswith("_rename.fna")]

for file in files:
	# contruct object
	file_obj = sc.Fasta(file, 'dataflow/01-nucl/')

	# set output name, location
	outputfilename = file.split(".f")[0] + '.faa'
	file_obj.setOutputName(outputfilename)
	file_obj.setOutputLocation('dataflow/01-prot/')

	# run prodigal
	file_obj.runprodigal()

files = [f for f in os.listdir(prot_dir) if f.endswith("_rename.faa")]

# these are the directories we are working with
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

# make blast db for each file
for file in files:
	file_obj = sc.Fasta(file, prot_dir)
	file_obj.setOutputName(file)
	file_obj.setOutputLocation(blastdbdir)
	file_obj.runmakeblastdb(dbtype='prot')

# blast database names
blastdbs = files.copy()

# blast all files against all blast databases (all against all)
for file in files:
	file_obj = sc.Fasta(file, prot_dir)
	file_obj.setOutputLocation(blastdir)
	for blastdb in blastdbs:
		outputfilename = file.split('.f')[0] + '.' + blastdb.split('.f')[0] + '.txt'
		file_obj.setOutputName(outputfilename)
		file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-3, num_threads = 60)
