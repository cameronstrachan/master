import os, sys
import pandas as pd


input_selected_species = 'dataflow/00-meta/ani_drep_ccoli_trim.csv'
df_selected_species = pd.read_csv(input_selected_species)

input_dir = 'dataflow/01-nucl/'
output_dir = 'dataflow/01-nucl/selected_genomes_coli/'
classification_dir = 'dataflow/02-classification/selected_genomes_coli/'


for index, row in df_selected_species.iterrows():
    file = row['genome1']
    input_file = input_dir + file
    command = 'cp ' + input_file + ' ' + output_dir

os.system("gtdbtk classify_wf --genome_dir dataflow/01-nucl/selected_genomes_coli --out_dir dataflow/02-classification/selected_genomes_coli --extension fa --cpus 60")
