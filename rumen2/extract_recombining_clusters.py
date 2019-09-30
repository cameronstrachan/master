# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('campylobacter_coli.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('campylobacter_coli_extracted_clusters.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.extract_regions(df = 'dataflow/03-analysis/cluster_positions_ccoli.csv', col_start = "cluster_start", col_end = "cluster_end", col_contig = "pathogen_genome_id")

file_obj = sc.Fasta('campylobacter_jejuni.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('campylobacter_jejuni_extracted_clusters.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.extract_regions(df = 'dataflow/03-analysis/cluster_positions_cjejuni.csv', col_start = "cluster_start", col_end = "cluster_end", col_contig = "pathogen_genome_id")
