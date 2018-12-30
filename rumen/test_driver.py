# python libraries
import os, sys
import subprocess
import pandas as pd
from itertools import islice

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg
from modules import seq_scrape as ss
from modules.ctb_functions import *

extractseqs = input("\n" + "Extract seqs with Lacto-Prevo correlations? (y or n):")

if extractseqs == 'y':

### select seq ids from metadata
	meta_df = pd.read_csv('dataflow/00-meta/henderson2015_lactobacillus_association.csv', low_memory=False)

	seqs_neg_cor = meta_df[meta_df['direction'] == 'neg_cor']
	seqs_neg_cor = seqs_neg_cor['asv_id'].tolist()


	seqs_pos_cor = meta_df[meta_df['direction'] == 'pos_cor']
	seqs_pos_cor = seqs_pos_cor['asv_id'].tolist()



	file_obj = sc.Fasta('henderson2015-1_315-97.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputLocation('dataflow/01-nucl/')

	file_obj.setOutputName('lacto_prevo_negative.fasta')
	file_obj.subsetfasta(seqlist = seqs_neg_cor , headertag='negative_correlation')

	file_obj.setOutputName('lacto_prevo_positive.fasta')
	file_obj.subsetfasta(seqlist = seqs_pos_cor, headertag='postive_correlation')


	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_prevo.fasta', filenames=["lacto_prevo_negative.fasta", "lacto_prevo_positive.fasta"])

runmakedb = input("\n" + "Make nucl blast database with asv seqs from Henderson 205 data? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('henderson2015-1_315-100.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputName('henderson2015-1_315-100_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()




runblast = input("\n" + "Blast Henderson 97 clustered asvs against 100 clustered asvs? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_prevo.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_prevo_100_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='henderson2015-1_315-100_db')


runblast = input("\n" + "Lacto-Prevo 100 blast? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_prevo_100.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_prevo_100_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='rumen_genomes_db')


runprodigal = input("\n" + "Run prodigal on selected Prevotella MAGS? (y or n):")

if runprodigal == 'y':

	files = ["GCF_000025925.1_ASM2592v1_genomic_rename.fasta",
"4300142-submission.assembly_rename.fasta",
"4300076-submission.assembly_rename.fasta",
"GCF_000762865.1_04_NF40_HMP671v01_genomic_rename.fasta",
"GCF_001553265.1_ASM155326v1_genomic_rename.fasta",
"GCF_000177075.1_ASM17707v1_genomic_rename.fasta",
"GCF_002884635.1_ASM288463v1_genomic_rename.fasta",
"GCF_000477535.1_PsaliF0493v1.0_genomic_rename.fasta",
"GCF_000185845.1_ASM18584v1_genomic_rename.fasta"]

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

	files = ["GCF_000025925.1_ASM2592v1_genomic_rename.fasta",
"4300142-submission.assembly_rename.fasta",
"4300076-submission.assembly_rename.fasta",
"GCF_000762865.1_04_NF40_HMP671v01_genomic_rename.fasta",
"GCF_001553265.1_ASM155326v1_genomic_rename.fasta",
"GCF_000177075.1_ASM17707v1_genomic_rename.fasta",
"GCF_002884635.1_ASM288463v1_genomic_rename.fasta",
"GCF_000477535.1_PsaliF0493v1.0_genomic_rename.fasta",
"GCF_000185845.1_ASM18584v1_genomic_rename.fasta"]

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

makeheadermap = input("\n" + "Make a header map? (y or n):")


if makeheadermap == 'y':

	files = ["GCF_000025925.1_ASM2592v1_genomic_rename.fasta",
"4300142-submission.assembly_rename.fasta",
"4300076-submission.assembly_rename.fasta",
"GCF_000762865.1_04_NF40_HMP671v01_genomic_rename.fasta",
"GCF_001553265.1_ASM155326v1_genomic_rename.fasta",
"GCF_000177075.1_ASM17707v1_genomic_rename.fasta",
"GCF_002884635.1_ASM288463v1_genomic_rename.fasta",
"GCF_000477535.1_PsaliF0493v1.0_genomic_rename.fasta",
"GCF_000185845.1_ASM18584v1_genomic_rename.fasta"]

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





prevgenomes = input("\n" + "Concatenate prevotella genomes and make blast db? (y or n):")

if prevgenomes == 'y':

	meta_df = pd.read_csv('dataflow/00-meta/prevotella_genomes.csv', low_memory=False)
	files = meta_df['file'].tolist()

	for file in files:	

		file_obj = sc.Fasta(file, "dataflow/01-nucl/")

		outfilename = file.split('.f')[0] + '_rename.fasta'

		file_obj.setOutputName(outfilename)
		file_obj.setOutputLocation("dataflow/01-nucl/")

		file_obj.headerrename()
	

	files_rename = [w.replace('.fna', '_rename.fasta') for w in files]


	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/prevotella_genomes.fasta', filenames=files_rename)

	file_obj = sc.Fasta('prevotella_genomes.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('prevotella_genomes_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()


runblast = input("\n" + "Lacto-Prevo 100 blast against prevotella? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_prevo_100.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_prevo_100_prevo_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=10, db='prevotella_genomes_db')