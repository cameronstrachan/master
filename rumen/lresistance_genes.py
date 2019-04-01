import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

# this is from the recent blast of all rumen genomes

# run prodigal

contigs = ['4309689-submission.assembly_79', '4309680-submission.assembly_52', 'RUG782_1']

file_obj = sc.Fasta('rumen_genomes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('rumen_genomes_resistance_genes.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.subsetfasta(seqlist = contigs, headertag='resistance_genes')

file_obj = sc.Fasta('rumen_genomes_resistance_genes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('rumen_genomes_resistance_genes.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal()


file = 'resistance_island_blast_hits_concatenated.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
outputfilename = file.split(".f")[0] + '_extractedCONTIGs' + '.fasta'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-nucl/')
#file_obj.extractORFs_gff3(gff3_table_loc = 'dataflow/00-meta/resistance_blast_hit_cotigs.csv')

indir = 'dataflow/01-nucl/'
headerfile = 'dataflow/02-headers/'


file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(headerfile)
headers = file_obj.fasta2headermap()
df = pd.DataFrame.from_dict(headers, orient="index")
df['file'] = file
df.to_csv(headerfile + file.split('.fa')[0] + '.csv')

# blast islands against rumen islands

file = "rumen_genomes_resistance_genes.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_mapping.txt"
blastdb = "rumen_genomes_resistance_genes.fasta"

file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=10, evalue=1e-3, num_threads = 60, max_hsps = 5)

# blast all islands against each other to find out which are the same


file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_mapping_allvall.txt"
blastdb = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=50, evalue=1e-3, num_threads = 60, max_hsps = 1)
