import os, sys
import pandas as pd


input_selected_species = 'dataflow/00-meta/ani_drep_ccoli_trim.csv'
df_selected_species = pd.read_csv(input_selected_species)

input_dir = 'dataflow/01-nucl/selected_genomes/'
output_dir = 'dataflow/01-nucl/selected_genomes_coli/'
classification_dir = 'dataflow/02-classification/selected_genomes_coli/'


for index, row in df_selected_species.iterrows():
    file = row['genome1']
    input_file = input_dir + file
    command = 'cp ' + input_file + ' ' + output_dir
    os.system(command)

command = 'cp dataflow/01-nucl/GCF_001687475.2_ASM168747v2_genomic.fna ' + output_dir + 'Chepaticus_outgroup.fna'
os.system(command)

#gtdbtk identify --genome_dir dataflow/01-nucl/selected_genomes_coli --out_dir dataflow/02-classification/selected_genomes_coli/identify --cpus 60
#gtdbtk align --identify_dir dataflow/02-classification/selected_genomes_coli/identify --out_dir dataflow/02-classification/selected_genomes_coli/align --skip_gtdb_refs --skip_trimming --cpus 60
#iqtree -s dataflow/02-classification/selected_genomes_coli/align/gtdbtk.bac120.user_msa.fasta -m TEST -bb 1000 -alrt 1000 -nt 70
