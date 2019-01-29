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

runrename = input("\n" + "Run renaming of selected (all prevotella) genomes? (y or n):")

if runrename == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
	genomes = genomes_df['BinID'].tolist()
	files = [item + ".fasta" for item in genomes]

	for file in files:	

			file_obj = sc.Fasta(file, "dataflow/01-nucl/")

			outfilename = file.split('.f')[0] + '_rename.fasta'

			file_obj.setOutputName(outfilename)
			file_obj.setOutputLocation("dataflow/01-nucl/")

			file_obj.headerrename()
	

runprodigal = input("\n" + "Run prodigal on selected Prevotella genomes? (y or n):")

if runprodigal == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
	genomes = genomes_df['BinID'].tolist()
	files = [item + "_rename.fasta" for item in genomes]

	for file in files:
		# contruct object
		file_obj = sc.Fasta(file, 'dataflow/01-nucl/')

		# set output name, location
		outputfilename = file.split(".f")[0] + '.fasta'
		file_obj.setOutputName(outputfilename)
		file_obj.setOutputLocation('dataflow/01-prot/')
		
		# run prodigal 
		file_obj.runprodigal()


runallvallblast = input("\n" + "Run all against all blast with Prevoltella genomes? (y or n):")

if runallvallblast == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
	genomes = genomes_df['BinID'].tolist()
	files = [item + "_rename.fasta" for item in genomes]

	# these are the directories we are working with
	indir = 'dataflow/01-prot/'
	blastdbdir = 'dataflow/02-blast-db/'
	blastdir = 'dataflow/02-blast/'

	# make blast db for each file
	for file in files:
		file_obj = sc.Fasta(file, indir)
		file_obj.setOutputName(file)
		file_obj.setOutputLocation(blastdbdir)
		file_obj.runmakeblastdb(dbtype='prot')

	# blast database names
	blastdbs = files.copy()

	# blast all files against all blast databases (all against all)
	for file in files:
		file_obj = sc.Fasta(file, indir)
		file_obj.setOutputLocation(blastdir)
		for blastdb in blastdbs:
			outputfilename = file.split('.f')[0] + '.' + blastdb.split('.f')[0] + '.txt'
			file_obj.setOutputName(outputfilename)
			file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-3, num_threads = 60)

makeheadermap = input("\n" + "Make a header map? (y or n):")


if makeheadermap == 'y':

	indir = 'dataflow/01-prot/'
	headerfile = 'dataflow/02-headers/'
	#header_dict = dict()

	for file in files:
		file_obj = sc.Fasta(file, indir)
		file_obj.setOutputName(file)
		file_obj.setOutputLocation(headerfile)
		
		headers = file_obj.fasta2headermap()

		df = pd.DataFrame.from_dict(headers, orient="index")

		df['file'] = file
		
		df.to_csv(headerfile + file.split('.fa')[0] + '.csv')