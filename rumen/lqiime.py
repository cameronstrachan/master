import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

### RUN QIIME HENDERSON 2015
### Environment: source activate qiime2-2018.11

downloaddata = input("\n" + "Download data from Sun et al 2019? (y or n):")

if downloaddata == 'y':

    accession_nums = list(range(326, 659, 1))
    accession_list = ['SRX4168' + str(x) for x in accession_nums]

    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/sun2019')

runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/sun2019', paired=False, numcores=60)

qiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=60)
