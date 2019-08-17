import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('extracted_regions.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('extracted_regions_oneLine.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.saveonelinefasta()

file_obj = sc.Fasta('extracted_regions_oneLine.fasta', 'dataflow/01-prot/')

file_obj.setOutputLocation('dataflow/02-blast/')
file_obj.runonlineblast(blasttype='blastp', database="nr", numhits=10, evalue=0.005)
