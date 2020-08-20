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

from modules import seq_core as sc

file_obj = sc.Fasta("cnoahi_unicycler_closed.ffn", 'dataflow/01-dbs/')
file_obj.setOutputName("cnoahi_unicycler_closed.ffn")
file_obj.setOutputLocation('dataflow/01-dbs/blastdbs/')
file_obj.runmakeblastdb(dbtype='nucl')


blastdbdir = 'dataflow/01-dbs/blastdbs/'
genes_input_folder = 'dataflow/02-genes/'
genome_extension = '.fasta'
blast_output_dir = 'dataflow/03-blast/cnoahi/'
gene_files = [f for f in os.listdir(genes_input_folder) if f.endswith(genome_extension)]
blastdb = 'cnoahi_unicycler_closed.ffn'

for file in gene_files:

    file_obj = sc.Fasta(file, genes_input_folder)
    file_obj.setOutputLocation(blast_output_dir)

    output_file = file.split(genome_extension)[0] + ':' + blastdb + '.txt'

    file_obj.setOutputName(output_file)
    file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-20, num_threads = 5)
