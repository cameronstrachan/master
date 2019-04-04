import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('rumen_genomes_resistance_genes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('rumen_genomes_resistance_genes.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal()

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='nucl')

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_mapping_allvall_V2.txt"
blastdb = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=500, evalue=1e-3, num_threads = 60, max_hsps = 10)


file = "rumen_genomes.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'

# blast resistance islands against all

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='nucl')

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen_all_genomes.txt"
blastdb = "rumen_genomes.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=500, evalue=1e-3, num_threads = 60, max_hsps = 10)


# extract all rumen resistance islands

file = 'rumen_genomes.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
outputfilename = file.split(".f")[0] + '_extractedCONTIGs_all_rumen' + '.fasta'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.extractORFs_gff3(gff3_table_loc = 'dataflow/00-meta/resistance_blast_hit_cotigs_all_rumen.csv')
