# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('lacto_signal_differential_seqs_genomes_16s.fasta', 'dataflow/02-16s/')
file_obj.setOutputName('lacto_signal_differential_seqs_genomes_16s.fasta')
file_obj.setOutputLocation('dataflow/02-16s/')

headers = file_obj.fasta2headermap()
l = []

for key, value in headers.items():
	if str(key[0:3]) == '16S':
		l.append(key)

file_obj.subsetfasta(seqlist = l , headertag='extracted')