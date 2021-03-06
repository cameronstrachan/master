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

<<<<<<< HEAD
# step 1 - trim rumen genes file those those above 300bp
file_obj = sc.Fasta('stewart2019_mags_genes_sub.fasta', blastin)
file_obj.setOutputName('stewart2019_mags_genes_sub_300.fasta')
file_obj.setOutputLocation(blastin)
file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'above')

# step 2 - loop through the different pathogen genome database files, blastn
blastdb = 'dataflow_test/02-blast-db/'
blastout = 'dataflow_test/02-blast-out/'
blastin = 'dataflow_test/01-nucl/'
input_file = 'stewart2019_mags_genes_sub.fasta'
dbs = ['campylobacter_coli.fasta', 'listeria_monocytogenes.fasta', 'staphylococcus_aureus.fasta']
output_files_blast = []

for db_file in dbs:
    file_obj = sc.Fasta(input_file, blastin)
    outname = input_file.split('.fa')[0] + '_' + df_file.split('.fa')[0] + '.txt'
    file_obj.setOutputName(outname)
    file_obj.setOutputLocation(blastout)
    #file_obj.runblast(blast='blastn', db=db_file, dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)
    output_files_blast.append(outname)

# step 3 - summarize frequency of hits
command = 'Rscript summarize_hit_frequency.R '
output_files_freq = []

for file in output_files:
    command = command + file + ' '
    outname = file.split('.tx')[0] + '.csv'
    output_files_freq.append(outname)

os.system(command)

# step 4 - extract genes from the frequency tables for annotation

genes = []
analysis_folder = 'dataflow_test/03-analysis/'
for file in output_files_freq:
    csv_file = analysis_folder + file
    df = pd.read_csv(csv_file, low_memory=False)
    gene_ids = df_seqs['gene'].tolist()
    genes.append(gene_ids)

genes_unique = set(genes)

file_obj = sc.Fasta(input_file, blastin)
outname = input_file.split('.fa')[0] + '_pathogen_mapped.fasta'
file_obj.setOutputName(outname)
file_obj.setOutputLocation(blastin)
file_obj.subsetfasta(seqlist = genes_unique, headertag='none')
=======
blastdb = 'dataflow_test/02-blast-db/'
blastout = 'dataflow_test/02-blast-out/'
blastin = 'dataflow_test/01-nucl/'

file_obj = sc.Fasta('metagenome_genes.fasta', blastin)
file_obj.setOutputName('metagenome_genes_300.fasta')
file_obj.setOutputLocation(blastin)
file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'above')

file_obj = sc.Fasta('metagenome_genes_300.fasta', blastin)
file_obj.setOutputName('metagenome_genes_campylobacter_coli.txt')
file_obj.setOutputLocation(blastout)
file_obj.runblast(blast='blastn', db='campylobacter_coli.fasta', dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)

#

file_obj = sc.Fasta('metagenome_genes_300.fasta', blastin)
file_obj.setOutputName('metagenome_genes_listeria_monocytogenes.txt')
file_obj.setOutputLocation(blastout)
file_obj.runblast(blast='blastn', db='listeria_monocytogenes.fasta', dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)

#

file_obj = sc.Fasta('metagenome_genes_300.fasta', blastin)
file_obj.setOutputName('metagenome_genes_staphylococcus_aureus.txt')
file_obj.setOutputLocation(blastout)
file_obj.runblast(blast='blastn', db='staphylococcus_aureus.fasta', dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)
>>>>>>> 5aa85ebf7c18269d0cd3a63ac22446d7dc2ed835
