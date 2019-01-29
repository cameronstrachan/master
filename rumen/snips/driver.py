# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg
from modules import seq_scrape as ss
from modules.ctb_functions import *

### DOWNLOAD FASTQs FOR Wetzels et al. 2017 (RUSITEC)

accession_nums = list(range(185, 221, 1))
accession_list = ['ERX1660' + str(x) for x in accession_nums]

download16s = input("\n" + "Download 16s data from Wetzels et al. 2017? (y or n):")

if download16s == 'y':
	for accession in accession_list:
		ss.srafastqdownlaod(accession, outputdir='dataflow/01-fastq/wetzels2018')

# rename the downloaded files so that they work with qiime
if download16s == 'y':
	fastq_path = 'dataflow/01-fastq/wetzels2018'
	i = 1

	for accession in accession_list:
		infilename = fastq_path + accession + '_pass.fastq.gz'
		outfilename = fastq_path + accession + '_' + str(i) + '_L001_R1_001.fastq.gz'
		i = i + 1
		os.rename(infilename, outfilename)


### DOWNLOAD FASTQs FOR Henderson et al. 2015 (Global rumen sequences)

accession_nums1 = list(range(4093, 6359, 1))
accession_list1 = ['SRX85' + str(x) for x in accession_nums1]

accession_nums2 = list(range(5542, 5578, 1))
accession_list2 = ['SRX85' + str(x) for x in accession_nums2]

accession_nums3 = list(range(3980, 4028, 1))
accession_list3 = ['SRX85' + str(x) for x in accession_nums3]

accession_list = accession_list1 + accession_list2 + accession_list3

download16s = input("\n" + "Download 16s data from Henderson et al. 2017? (y or n):")

if download16s == 'y':
	for accession in accession_list:
		ss.srafastqdownlaod(accession, outputdir='dataflow/01-fastq/henderson2015')

# rename the downloaded files so that they work with qiime
if download16s == 'y':
	fastq_path = 'dataflow/01-fastq/henderson2015/'
	i = 1

	for accession in accession_list:
		infilename = fastq_path + accession + '_pass.fastq.gz'
		outfilename = fastq_path + accession + '_' + str(i) + '_L001_R1_001.fastq.gz'
		i = i + 1
		os.rename(infilename, outfilename)


### RUN QIIME
runqiime = input("\n" + "Run Qiime on data from Wetzels et al. 2017? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/wetzels2018', paired=False, numcores=7)

### RUN QIIME
runqiime = input("\n" + "Run Qiime on data from Reddy et al. 2018? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/reddy2018', paired=True, numcores=7)

### RUN QIIME
runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=7)


### EXTRACT 16s sequences from genomes

extract16s = input("\n" + "Extract 16s from all files in 01-nucl? (y or n):")

if extract16s == 'y':

	indir = 'dataflow/01-nucl/'
	files_all = [f for f in os.listdir(indir) if f.endswith(tuple([".fasta", ".fa", ".fna"]))]
	files = [ p for p in files_all if not(p.startswith('.'))]

	for file in files:

		file_obj = sc.Fasta(file, indir)

		outfilename = file.split('.f')[0] + '_16s.fasta'

		file_obj.setOutputName(outfilename)
		file_obj.setOutputLocation('dataflow/02-16s/')

		file_obj.extract16s()

concatenate16s = input("\n" + "Concatenate 16s from all files in 02-16s? (y or n):")

if concatenate16s == 'y':

	indir = 'dataflow/02-16s/'
	files_all = [f for f in os.listdir(indir) if f.endswith(tuple([".fasta", ".fa", ".fna"]))]
	files = [ p for p in files_all if not(p.startswith('.'))]

	for file in files:	

		file_obj = sc.Fasta(file, indir)

		outfilename = file.split('.f')[0] + '_rename.fasta'

		file_obj.setOutputName(outfilename)
		file_obj.setOutputLocation(indir)

		file_obj.headerrename()

	
	files_all = [f for f in os.listdir(indir) if f.endswith("_rename.fasta")]
	files = [p for p in files_all if not(p.startswith('.'))]

	sg.concat('dataflow/02-16s/', 'dataflow/02-16s/all_16s.fasta', files)

	file_obj = sc.Fasta('all_16s.fasta', indir)
	file_obj.setOutputName('all_16s_below2000.fasta')
	file_obj.setOutputLocation(indir)

	file_obj.lengthcutoff(replaceheaders = False, length = 2000, direction = 'below')

### DOWNLOAD GENOMES AND MAKE FASTA FILES

downloadgenomes = input("\n" + "Download complete bacteroides ovatus genomes? (y or n):")

if downloadgenomes == 'y':

	gb_dir = 'dataflow/01-gb/'
	ss.ncbigenomescrape('bacteroides ovatus', location=gb_dir)
	gb_prot_out = 'dataflow/01-prot/'
	gb_nucl_out = 'dataflow/01-nucl/'
	extention_add = '_genbank.fasta'

	files = [f for f in os.listdir(gb_dir) if f.endswith(".gb")]

	for file in files:
		file_obj = sc.GenBank(file, gb_dir)
		# output location
		file_obj.setOutputLocation(gb_prot_out)

		# output name
		file_out = file.split('.g')[0] + extention_add
		file_obj.setOutputName(file_out)

		# run genbank to prot
		file_obj.genbank2protfasta()


concatenate_nucl = input("\n" + "Concatenate all files in 01-nucl? (y or n):")

if concatenate_nucl == 'y':

	indir = 'dataflow/01-nucl/'
	files_all = [f for f in os.listdir(indir) if f.endswith(tuple([".fasta", ".fa", ".fna"]))]
	files = [ p for p in files_all if not(p.startswith('.'))]

	for file in files:	

		file_obj = sc.Fasta(file, indir)

		outfilename = file.split('.f')[0] + '_rename.fasta'

		file_obj.setOutputName(outfilename)
		file_obj.setOutputLocation(indir)

		file_obj.headerrename()

	
	files_all = [f for f in os.listdir(indir) if f.endswith("_rename.fasta")]
	files = [p for p in files_all if not(p.startswith('.'))]

	sg.concat('dataflow/01-nucl/', 'dataflow/01-nucl/rumen_genomes.fasta', files)

runmakedb = input("\n" + "Make nucl blast database with rumen genomes data? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('rumen_genomes.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('rumen_genomes_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()

runblast = input("\n" + "5 provo blast? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('5_prevotellaceae.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('5_prevotellaceae_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='rumen_genomes_db')



runprodigal = input("\n" + "Run prodigal on selected Prevotella genomes? (y or n):")

if runprodigal == 'y':

	files = ["4302445-submission.assembly_rename.fasta", "3353505-final.assembly_rename.fasta", "4304392-submission.assembly_rename.fasta", "GCF_900110745.1_IMG-taxon_2693429877_annotated_assembly_genomic_rename.fasta", "4300142-submission.assembly_rename.fasta", "4300076-submission.assembly_rename.fasta", "4309559-submission.assembly_rename.fasta"]

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

	files = ["4302445-submission.assembly_rename.fasta", "3353505-final.assembly_rename.fasta", "4304392-submission.assembly_rename.fasta", "GCF_900110745.1_IMG-taxon_2693429877_annotated_assembly_genomic_rename.fasta", "4300142-submission.assembly_rename.fasta", "4300076-submission.assembly_rename.fasta", "4309559-submission.assembly_rename.fasta"]

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


if makeheadermap== 'y':

	files = ["4302445-submission.assembly_rename.fasta", "3353505-final.assembly_rename.fasta", "4304392-submission.assembly_rename.fasta", "GCF_900110745.1_IMG-taxon_2693429877_annotated_assembly_genomic_rename.fasta", "4300142-submission.assembly_rename.fasta", "4300076-submission.assembly_rename.fasta", "4309559-submission.assembly_rename.fasta"]

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

