import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

contigs = ['4309689-submission.assembly_79', '4309680-submission.assembly_52', 'RUG782_1']

file_obj = sc.Fasta('rumen_genomes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('rumen_genomes_resistance_genes.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.subsetfasta(seqlist = contigs, headertag='resistance_genes')

file_obj = sc.Fasta('rumen_genomes_resistance_genes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('rumen_genomes_resistance_genes.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.runprodigal()


file = 'resistance_island_blast_hits_concatenated.fasta'
file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
outputfilename = file.split(".f")[0] + '_extractedCONTIGs' + '.fasta'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.extractORFs_gff3(gff3_table_loc = 'dataflow/00-meta/resistance_blast_hit_cotigs.csv')
