# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

srafastqdownlaod('SRX1585089', outputdir='dataflow/01-fastq/marre2017')
