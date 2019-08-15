# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg


files = ['n_gracillis_rename.fna', 'n_noahi_rename.fna', 'n_stinkeri_rename.fna']

sg.concat(inputfolder='dataflow/01-prot/', outputpath='dataflow/01-prot/nitrospinae_genomes.fasta', filenames=files)

genes_df = pd.read_csv('extracted_regions_genes.csv', low_memory=False)
genes = genes_df['qseqid'].tolist()

file_obj = sc.Fasta('nitrospinae_genomes.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('extracted_regions.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.subsetfasta(seqlist = genes, headertag='extracted_regions')
