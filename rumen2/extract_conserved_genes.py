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

blastdb = 'dataflow_test/02-blast-db/'
blastout = 'dataflow_test/02-blast-out/'
blastin = 'dataflow_test/01-nucl/'
input_file = 'stewart2019_mags_genes_sub.fasta'
dbs = ['campylobacter_coli.fasta', 'listeria_monocytogenes.fasta', 'staphylococcus_aureus.fasta']
output_files_blast = []

# step 1 - trim rumen genes file those those above 300bp
file_obj = sc.Fasta('stewart2019_mags_genes_sub.fasta', blastin)
file_obj.setOutputName('stewart2019_mags_genes_sub_300.fasta')
file_obj.setOutputLocation(blastin)
#file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'above')

# step 2 - loop through the different pathogen genome database files, blastn
for db_file in dbs:
    file_obj = sc.Fasta(input_file, blastin)
    outname = input_file.split('.fa')[0] + '_' + db_file.split('.fa')[0] + '.txt'
    file_obj.setOutputName(outname)
    file_obj.setOutputLocation(blastout)
    #file_obj.runblast(blast='blastn', db=db_file, dblocation=blastdb, max_target_seqs=5000, evalue=1e-100, num_threads = 60, max_hsps = 1)
    output_files_blast.append(outname)

# step 3 - summarize frequency of hits
command = 'Rscript summarize_hit_frequency.R '
output_files_freq = []

for file in output_files_blast:
    command = command + file + ' '
    outname = file.split('.tx')[0] + '.csv'
    output_files_freq.append(outname)

os.system(command)

# step 4 - extract genes from the frequency tables for annotation and convert to ORFS
genes = []
analysis_folder = 'dataflow_test/03-analysis/'
for file in output_files_freq:
    csv_file = analysis_folder + file
    df = pd.read_csv(csv_file, low_memory=False)
    gene_ids = df['gene'].tolist()
    genes = genes + gene_ids

genes_unique = list(set(genes))

file_obj = sc.Fasta(input_file, blastin)
outname = input_file.split('.fa')[0] + '_pathogen_mapped.fasta'
file_obj.setOutputName(outname)
file_obj.setOutputLocation(blastin)
file_obj.subsetfasta(seqlist = genes_unique, headertag='none')

file_obj = sc.Fasta(outname, 'dataflow_test/01-nucl/')
file_obj.setOutputName(outname)
file_obj.setOutputLocation('dataflow_test/01-prot/')
file_obj.translateORFs()

# step 5 - annotate the ORFs
file_obj = sc.Fasta(outname, 'dataflow_test/01-prot/')
file_obj.setOutputLocation('dataflow_test/02-blast-xml/')
#file_obj.runonlineblast(numhits=1)

blastfiles = [outname]
xmlfiles = [f for f in os.listdir('dataflow_test/02-blast-xml') if f.endswith(".xml")]
sg.blastxmltotable(xmlinputfolder='dataflow_test/02-blast-xml/', blastinputfolder='dataflow_test/01-nucl/',outputpath='dataflow_test/03-analysis/compiled_annotations.txt', xmlfilenames=xmlfiles, blastfilename=blastfiles)

# make header map file to extract locations of genes
