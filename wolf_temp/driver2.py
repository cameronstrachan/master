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



### RUN QIIME
#runqiime = input("\n" + "Run Qiime on data from Wetzels et al. 2018? (y or n):")

#if runqiime == 'y':
#	sg.runqiime(inputfolderloc='dataflow/01-fastq/wetzels2018', paired=True, numcores=7)


accession_nums1 = list(range(1, 10, 1))
accession_list1 = ['SRR429490' + str(x) for x in accession_nums1]

accession_nums2 = list(range(10, 55, 1))
accession_list2 = ['SRR42949' + str(x) for x in accession_nums2]

accession_list = accession_list1 + accession_list2


#download16s = input("\n" + "Download 16s data from Wetzels et al. 2017? (y or n):")
#
#if download16s == 'y':
#	for accession in accession_list:
#		ss.srafastqdownlaod(accession, outputdir='dataflow/01-fastq/wu2018')

#fastq_path = 'dataflow/01-fastq/wu2018/'
#i = 1

#for accession in accession_list:
#	infilename = fastq_path + accession + '_pass.fastq.gz'
#	outfilename = fastq_path + accession + '_' + str(i) + '_L001_R1_001.fastq.gz'
#	i = i + 1
#	os.rename(infilename, outfilename)


### RUN QIIME
#runqiime = input("\n" + "Run Qiime on data from Wu et al. 2017? (y or n):")

#if runqiime == 'y':
sg.runqiime(inputfolderloc='dataflow/01-fastq/wu2018', paired=False, numcores=7)