# python libraries
import os, sys
import subprocess

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg
from modules import seq_scrape as ss

### DOWNLOAD FASTQs FOR Wetzels et al. 2017 (RUSITEC)

accession_nums = list(range(185, 221, 1))
accession_list = ['ERX1660' + str(x) for x in accession_nums]

download16s = input("\n" + "Download 16s data from Wetzels et al. 2017? (y or n):")

if download16s == 'y':
	for accession in accession_list:
		ss.srafastqdownlaod(accession)

# rename the downloaded files so that they work with qiime
if download16s == 'y':
	fastq_path = 'dataflow/01-fastq/'
	i = 1

	for accession in accession_list:
		infilename = fastq_path + accession + '_pass.fastq.gz'
		outfilename = fastq_path + accession + '_' + str(i) + '_L001_R1_001.fastq.gz'
		i = i + 1
		os.rename(infilename, outfilename)

### RUN QIIME
runqiime = input("\n" + "Run Qiime on data from Wetzels et al. 2017? (y or n):")

if runqiime == 'y':
	subprocess.call('/Users/cameronstrachan/master/bash/run_qiime.sh')
	subprocess.call('/Users/cameronstrachan/master/bash/qiime_export.sh')
	os.rename('dataflow/03-asv-seqs/dna-sequences-100.fasta', 'dataflow/03-asv-seqs/wetzels2017-100.fasta')
	os.rename('dataflow/03-asv-seqs/dna-sequences-99.fasta', 'dataflow/03-asv-seqs/wetzels2017-99.fasta')
	os.rename('dataflow/03-asv-seqs/dna-sequences-97.fasta', 'dataflow/03-asv-seqs/wetzels2017-97.fasta')
	os.rename('dataflow/03-asv-table/feature-table-100.txt', 'dataflow/03-asv-table/wetzels2017-100.txt')
	os.rename('dataflow/03-asv-table/feature-table-99.txt', 'dataflow/03-asv-table/wetzels2017-99.txt')
	os.rename('dataflow/03-asv-table/feature-table-97.txt', 'dataflow/03-asv-table/wetzels2017-97.txt')


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

		# output location
		file_obj.setOutputLocation(gb_nucl_out)

		# run genbank to prot
		file_obj.genbank2nuclfasta()