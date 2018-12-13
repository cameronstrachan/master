# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
#from modules import seq_scrape as ss
#from modules.ctb_functions import *



### RUN QIIME
runqiime = input("\n" + "Run Qiime on data from Wetzels et al. 2018? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/wetzels2018', paired=True, numcores=24)

### RUN QIIME
runqiime = input("\n" + "Run Qiime on data from Wu et al. 2017? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/wu2017', paired=False, numcores=24)

### RUN QIIME
runmerge = input("\n" + "Run merge on wetzels and wu? (y or n):")

if runmerge == 'y':
	sg.runqiimemerge(file1folder='wetzels2018', file2folder='wu2018')