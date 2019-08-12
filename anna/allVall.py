# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN PREVOTELLA ALL AGAINST ALL
### Environment: source activate qiime2-2018.11

nucl_dir = 'dataflow/01-nucl/'
prot_dir = 'dataflow/01-prot/'

runrename = input("\n" + "Rename Nitrospinae genomes? (y or n):")

if runrename == 'y':

	files = [f for f in os.listdir(nucl_dir) if f.endswith(".fasta")]
	print(files)

	for file in files:

		file_obj = sc.Fasta(file, "dataflow/01-nucl/")

		outfilename = file.split('.f')[0] + '_rename.fasta'

		file_obj.setOutputName(outfilename)
		file_obj.setOutputLocation("dataflow/01-nucl/")
		file_obj.headerrename()


runprodigal = input("\n" + "Run prodigal Nitrospinae genomes? (y or n):")

if runprodigal == 'y':

	files = [f for f in os.listdir(nucl_dir) if f.endswith("_rename.fasta")]

	for file in files:
		# contruct object
		file_obj = sc.Fasta(file, 'dataflow/01-nucl/')

		# set output name, location
		outputfilename = file.split(".f")[0] + '.fasta'
		file_obj.setOutputName(outputfilename)
		file_obj.setOutputLocation('dataflow/01-prot/')

		# run prodigal
		file_obj.runprodigal()

runallvallblast = input("\n" + "Run all against all blast with Nitrospinae genomes? (y or n):")

if runallvallblast == 'y':

	files = [f for f in os.listdir(prot_dir) if f.endswith("_rename.fasta")]

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

makeheadermap = input("\n" + "Make a header map with Nitrospinae genomes? (y or n):")
#makeheadermap = 'y'

if makeheadermap == 'y':

	headerfile = 'dataflow/02-headers/'

	for file in files:
		file_obj = sc.Fasta(file, prot_dir)
		file_obj.setOutputName(file)
		file_obj.setOutputLocation(headerfile)

		headers = file_obj.fasta2headermap()

		df = pd.DataFrame.from_dict(headers, orient="index")
		df['file'] = file
		df.to_csv(headerfile + file.split('.fa')[0] + '.csv')
