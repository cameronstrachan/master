import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

# ant6 from rumen

file_obj = sc.Fasta('ANT6_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_rumen_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'above')

file_obj = sc.Fasta('ANT6_rumen_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_rumen_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 350, direction = 'below')

# ant6 from ncbi

file_obj = sc.Fasta('ANT6_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_ncbi_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'above')

file_obj = sc.Fasta('ANT6_ncbi_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_ncbi_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 350, direction = 'below')
