import os, sys
from Bio.Seq import Seq
import pandas as pd

sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc

file = 'all_nitrospina_genomes.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
outputfilename = file.split(".f")[0] + '_extractedORFs' + '.fasta'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-prot/genes/')
file_obj.extractORFs_gff3(gff3_table_loc = 'dataflow/00-meta/all_nitrospina_genomes.csv')
