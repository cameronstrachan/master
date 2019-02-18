import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### Environment: source activate anaconda to dowload data

### RUN QIIME HENDERSON 2015
### Environment: source activate qiime2-2018.11

runqiime = input("\n" + "Run Qiime on data from Sun et al. 2019 (switch env qiime2-2018.11)? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/sun2019', paired=False, numcores=60)

runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (switch env qiime2-2018.11)(y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=60)


#for f in *.fastq.gz; do mv -- "$f" "${f//_pass/_1_L001_R1_001}"; done
