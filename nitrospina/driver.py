# python libraries
import os, sys
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg

renamefiles = input("\n" + "Rename on all files in 01-nucl? (y or n):")

if renamefiles == 'y':
	files_all = [f for f in os.listdir('dataflow/01-nucl/') if f.endswith(".fna")]
	# remove masked files (starting with '.')
	files = [p for p in files_all if not(p.startswith('.'))]

	for file in files:
		# contruct object
		file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
		file_obj.setOutputName(file.split('.f')[0] + '.rename.fna')
		file_obj.setOutputLocation('dataflow/01-nucl/')
		
		# run rename
		file_obj.headerrename()

runprodigal = input("\n" + "Run prodigal on all files in 01-nucl? (y or n):")

if runprodigal == 'y':
	files_all = [f for f in os.listdir('dataflow/01-nucl/') if f.endswith("rename.fna")]
	# remove masked files (starting with '.')
	files = [p for p in files_all if not(p.startswith('.'))]

	for file in files:
		# contruct object
		file_obj = sc.Fasta(file, 'dataflow/01-nucl/')

		# set output name, location
		outputfilename = file.split(".f")[0] + '.fasta'
		file_obj.setOutputName(outputfilename)
		file_obj.setOutputLocation('dataflow/01-prot/')
		
		# run prodigal 
		file_obj.runprodigal()




runallvallblast = input("\n" + "Run all against all blast? (y or n):")

if runallvallblast == 'y':

	# list all the fasta files in the protein directory
	files_all = [f for f in os.listdir('dataflow/01-prot/') if f.endswith(".fasta")]
	# remove masked files (starting with '.')
	files = [p for p in files_all if not(p.startswith('.'))]

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
			file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-3)

# list all the fasta files in the protein directory
files_all = [f for f in os.listdir('dataflow/01-prot/') if f.endswith("rename.fasta")]
# remove masked files (starting with '.')
files = [p for p in files_all if not(p.startswith('.'))]

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


# with open('dataflow/02-headers/nitrospina_genome_headers.csv', 'w') as csv_file:
# 	writer = csv.writer(csv_file)
# 	for key, value in header_dict.items():
# 		writer.writerow([key, value])

	