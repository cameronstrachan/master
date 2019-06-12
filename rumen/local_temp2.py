import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO
import numpy as np
from Bio import SearchIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg


f = open("dataflow/02-blast/orf_fig1_fig3_fig4.txt", "r")
o = open("dataflow/02-blast/orf_fig1_fig3_fig4_parsed.txt", "w")

for x in f:
    if x.startswith('Query= '):
        o.write(x + '\n')

    if ".1" in x and "   " in x:
        o.write(x + '\n')
