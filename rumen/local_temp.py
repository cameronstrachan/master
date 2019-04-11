import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

# ant6 from ncbi

file_obj = sc.Fasta('ANT6_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_ncbi_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'above')

file_obj = sc.Fasta('ANT6_ncbi_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_ncbi_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 350, direction = 'below')

# aph6 from ncbi

file_obj = sc.Fasta('APH3_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_ncbi_200.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 200, direction = 'above')

file_obj = sc.Fasta('APH3_ncbi_200.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_ncbi_200_300.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'below')

# sat4 from ncbi

file_obj = sc.Fasta('SAT4_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_ncbi_150.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 150, direction = 'above')

file_obj = sc.Fasta('SAT4_ncbi_150.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_ncbi_150_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'below')


# ant6 from rumen

file_obj = sc.Fasta('ANT6_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_rumen_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'above')

file_obj = sc.Fasta('ANT6_rumen_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_rumen_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 350, direction = 'below')

# aph6 from rumen

file_obj = sc.Fasta('APH3_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_rumen_200.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 200, direction = 'above')

file_obj = sc.Fasta('APH3_rumen_200.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_rumen_200_300.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'below')

# sat4 from rumen

file_obj = sc.Fasta('SAT4_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_rumen_150.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 150, direction = 'above')

file_obj = sc.Fasta('SAT4_rumen_150.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_rumen_150_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'below')
