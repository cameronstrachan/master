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
	os.rename('dataflow/03-asv-seqs/dna-sequences.fasta', 'dataflow/03-asv-seqs/wetzels2017.fasta')
	os.rename('dataflow/03-asv-table/feature-table.txt', 'dataflow/03-asv-table/wetzels2017.txt')