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

pathogen_dbs = ['staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis']

blastdbdir = 'dataflow/01-dbs/blastdbs/'

genes_input_folder = 'dataflow/03-selected-genes/'
genome_extension = '.fasta'
blast_output_dir = 'dataflow/03-blast/pathogens/'

gene_files = [f for f in os.listdir(prots_input_folder) if f.endswith(genome_extension)]


for file in gene_files:

    for blastdb in pathogen_dbs:

        file_obj = sc.Fasta(file, genes_input_folder)
        file_obj.setOutputLocation(blast_output_dir)

        output_file = file.split(genome_extension)[0] + '_' + blastdb + '.txt'

        file_obj.setOutputName(output_file)
        file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=50000, evalue=1e-20, num_threads = 60)
