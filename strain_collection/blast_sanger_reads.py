import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('sanger_strain_library.fasta', '01-nucl/')
file_obj.setOutputName('sanger_strain_library_oneLine.fasta')
file_obj.setOutputLocation('01-nucl/')
file_obj.saveonelinefasta()

file_obj = sc.Fasta('sanger_strain_library_oneLine.fasta', '01-nucl/')

file_obj.setOutputLocation('02-blast/')
#file_obj.runonlineblast(blasttype='blastn', database="nr", numhits=50, evalue=0.005)
