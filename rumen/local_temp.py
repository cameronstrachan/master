import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('aph3_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('aph3_ncbi_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = True, length = 250, direction = 'above')

file_obj = sc.Fasta('aph3_ncbi_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('aph3_ncbi_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = True, length = 350, direction = 'below')

file_obj = sc.Fasta('APH3_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_rumen_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = True, length = 250, direction = 'above')

file_obj = sc.Fasta('APH3_rumen_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_rumen_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = True, length = 350, direction = 'below')
