import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('core_epithelial_microbiome_99_oneline.fasta', 'dataflow/01-nucl/')

file_obj.setOutputLocation('dataflow/02-blast-online/')
file_obj.runonlineblast(blasttype='blastn', database="nr", numhits=50, evalue=0.005)
