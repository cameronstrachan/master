# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN QIIME ON HENDERSON DATA
runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=40)


### THEN ANALYSIS WITH DESeq_henderson2015_97 Rmardown

extractseqs = input("\n" + "Extract seqs with differential abundance between sample defined on the presence of Lactobacillus? (y or n):")

if extractseqs == 'y':

### select seq ids from metadata
	meta_df = pd.read_csv('dataflow/00-meta/lacto_signal_differential.csv', low_memory=False)

	seqs_decrease = meta_df[meta_df['direction'] == 'decrease']
	seqs_decrease = seqs_decrease['asv_id'].tolist()


	seqs_increase = meta_df[meta_df['direction'] == 'increase']
	seqs_increase = seqs_increase['asv_id'].tolist()



	file_obj = sc.Fasta('henderson2015-4_194-99.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputLocation('dataflow/01-nucl/')

	file_obj.setOutputName('lacto_prevo_decrease.fasta')
	file_obj.subsetfasta(seqlist = seqs_decrease , headertag='decrease')

	file_obj.setOutputName('lacto_prevo_increase.fasta')
	file_obj.subsetfasta(seqlist = seqs_increase, headertag='increase')


	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_signal_differential_seqs.fasta', filenames=["lacto_prevo_decrease.fasta", "lacto_prevo_increase.fasta"])


### THIS GOES FROM THE (97% seqs to the 100% seqs)

runmakedb = input("\n" + "Make nucl blast database with asv seqs from Henderson 2015 data (trimmed at 4 and 194)? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('henderson2015-4_194-100.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputName('henderson2015-4_194-100_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()

runblast = input("\n" + "Blast Henderson 97 clustered asvs against 100 clustered asvs (trimmed at 4 and 194)? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_seqs_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='henderson2015-4_194-100_db')

runscript = input("\n" + "Extract the representative seqs from the blast table? (y or n):")

if runscript == 'y':
	os.system("python src/python/representative2relatedseqs.py")

runblast = input("\n" + "Blast the 100 percent seqs against rumen genomes? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_all_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_tags_rumen_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='rumen_genomes_db')


runblast = input("\n" + "Blast the 100 percent seqs against prevotella genomes? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_all_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_tags_prevotella_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=10, db='prevotella_genomes_db')

runscript = input("\n" + "Extract the genomes seqs from the blast table? (y or n):")

if runscript == 'y':
	os.system("python src/python/blasttables2seqs.py")

runblast = input("\n" + "Concatenate sequences from genomes and Prevotella? (y or n):")

if runblast == 'y':
	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes.fasta', filenames=["lacto_signal_differential_all_seqs_genomes.fasta", "lacto_signal_differential_all_seqs_tags.fasta"])

runcommand = input("\n" + "Run muscle? (y or n):")

if runcommand == 'y':
	os.system("../bin/muscle -in dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes.fasta -out dataflow/03-alignments/lacto_signal_differential_all_seqs_tags_genomes_alignment.afa")

runcommand = input("\n" + "Run Gblocks? (y or n):")

if runcommand == 'y':
	os.system("../bin/Gblocks dataflow/03-alignments/lacto_signal_differential_all_seqs_tags_genomes_alignment.afa -t=d -b6=n")

runcommand = input("\n" + "Run FastTree? (y or n):")

if runcommand == 'y':
	os.system("../bin/FastTree -gtr -nt dataflow/03-alignments/lacto_signal_differential_all_seqs_tags_genomes_alignment.afa-gb > dataflow/03-trees/lacto_signal_differential_all_seqs_tags_genomes_tree.newick")


#####

runrename = input("\n" + "Run renaming of selected genomes? (y or n):")

if runrename == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/selected_genomes.csv', low_memory=False)
	genomes = genomes_df['Genome'].tolist()

	files = [item + ".fasta" for item in genomes]

	for file in files:	

			file_obj = sc.Fasta(file, "dataflow/01-nucl/")

			outfilename = file.split('.f')[0] + '_rename.fasta'

			file_obj.setOutputName(outfilename)
			file_obj.setOutputLocation("dataflow/01-nucl/")

			file_obj.headerrename()
	

runprodigal = input("\n" + "Run prodigal on selected Prevotella genomes? (y or n):")

if runprodigal == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/selected_genomes.csv', low_memory=False)
	genomes = genomes_df['Genome'].tolist()
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

	genomes_df = pd.read_csv('dataflow/00-meta/selected_genomes.csv', low_memory=False)
	genomes = genomes_df['Genome'].tolist()
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
		
		df.to_csv(headerfile + file.splslit('.fa')[0] + '.csv')

runcommand = input("\n" + "Run 16s search? (y or n):")

if runcommand == 'y':

	l = list()

	genomes_df = pd.read_csv('dataflow/00-meta/selected_genomes.csv', low_memory=False)
	genomes = genomes_df['Genome'].tolist()
	files = [item + "_rename.fasta" for item in genomes]

	for file in files:
		outputfile = file.split('.fa')[0] + "_16s.fasta"
		command = '../../barrnap/bin/barrnap --threads 20 --kingdom bac -o dataflow/02-16s/' + outputfile + ' < ' + 'dataflow/01-nucl/' + file
		os.system(command)
		l.append(outputfile)

	sg.concat(inputfolder='dataflow/02-16s/', outputpath='dataflow/02-16s/lacto_signal_differential_seqs_genomes_16s.fasta', filenames=l)

	file_obj = sc.Fasta('lacto_signal_differential_seqs_genomes_16s.fasta', 'dataflow/02-16s/')
	file_obj.setOutputName('lacto_signal_differential_seqs_genomes_16s_extracted.fasta')
	file_obj.setOutputLocation('dataflow/02-16s/')

	headers = file_obj.fasta2headermap()
	l = []

	for key, value in headers.items():
		if str(key[0:3]) == '16S':
			l.append(key)

	file_obj.subsetfasta(seqlist = l , headertag='number', replace=':', length=30)
	
	file_obj = sc.Fasta('lacto_signal_differential_seqs_genomes_16s_extracted.fasta', 'dataflow/02-16s/')
	file_obj.setOutputLocation('dataflow/02-16s/')
	file_obj.setOutputName('lacto_signal_differential_seqs_genomes_16s_extracted_1300.fasta')
	file_obj.lengthcutoff(replaceheaders = False, length = 1300, direction = 'above')

	file_obj.subsetfasta(seqlist = l , headertag='number', replace=':')
	file_obj = sc.Fasta('lacto_signal_differential_seqs_genomes_16s_extracted_1300.fasta', 'dataflow/02-16s/')
	file_obj.setOutputLocation('dataflow/02-16s/')
	file_obj.setOutputName('lacto_signal_differential_seqs_genomes_16s_extracted_1300_1700.fasta')
	file_obj.lengthcutoff(replaceheaders = False, length = 1700, direction = 'below')


runcommand = input("\n" + "Run muscle on full 16s seqs? (y or n):")

if runcommand == 'y':
	os.system("../bin/muscle -in dataflow/02-16s/lacto_signal_differential_seqs_genomes_16s_extracted_1300_1700.fasta -out dataflow/03-alignments/lacto_signal_differential_seqs_genomes_16s_extracted_1300_1700.afa")

runcommand = input("\n" + "Run Gblocks on full 16s seqs? (y or n):")

if runcommand == 'y':
	os.system("../bin/Gblocks dataflow/03-alignments/lacto_signal_differential_seqs_genomes_16s_extracted_1300_1700.afa -t=d -b6=n")

runcommand = input("\n" + "Run FastTree on full 16s seqs? (y or n):")

if runcommand == 'y':
	os.system("../bin/FastTree -gtr -nt dataflow/03-alignments/lacto_signal_differential_seqs_genomes_16s_extracted_1300_1700.afa-gb > dataflow/03-trees/lacto_signal_differential_seqs_genomes_16s_extracted_1300_1700.afa.newick")

