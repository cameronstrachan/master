import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

### Environment: source activate anaconda to dowload data

downloaddata = input("\n" + "Download test data? (y or n):")

if downloaddata == 'y':

    accession_nums = list(range(57, 61, 1))
    accession_list = ['SRX18539' + str(x) for x in accession_nums]

    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/test')
