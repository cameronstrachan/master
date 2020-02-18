import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('Pacbio_seqs.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('Pacbio_seqs_oneLine.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.saveonelinefasta()

file_obj = sc.Fasta('Pacbio_seqs_oneLine.fasta', 'dataflow/01-nucl/')

file_obj.setOutputLocation('dataflow/02-xml/')
file_obj.runonlineblast(blasttype='blastn', database="nr", numhits=1, evalue=0.000005)
