import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN QIIME HENDERSON 2015
### Environment: source activate qiime2-2018.11

runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=60)