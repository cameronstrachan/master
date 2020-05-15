# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/ar/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/ar/')

file = "card_db.fasta"
output_db = "card"
input_database_file = 'dataflow/01-dbs/CARD/'
blastdbdir = 'dataflow/01-dbs/'

file_obj = sc.Fasta(file, input_database_file)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='prot')

prots_input_folder = 'dataflow/02-prots/'
genome_extension = '.fasta'
blastdb = "card"
blast_output_dir = 'dataflow/03-blast/CARD/'

prot_files = [f for f in os.listdir(prots_input_folder) if f.endswith(genome_extension)]


for file in prot_files:

    file_obj = sc.Fasta(file, prots_input_folder)
    file_obj.setOutputLocation(blast_output_dir)

    output_file = file.split(genome_extension)[0] + '_' + blastdb + '.txt'

    file_obj.setOutputName(output_file)
    file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-5, num_threads = 60)
