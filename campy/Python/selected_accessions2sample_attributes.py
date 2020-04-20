import pandas as pd
import os, sys
import subprocess

# script to downloaded biosample ids from a search term from assembly database, match them with a dataframe of accesion numbers, and then download
# attributes from the biosample database

# HARDCODED
# select a search term for the assembly database that will ensure you get all of the samples for the genomes you are looking at
search_term = '\'\"Campylobacter\"[Organism]\''
output_acc_sample_mapping = 'dataflow/00-meta/campylobacter_sample_accession_map.txt'
input_selected_genus = 'dataflow/00-meta/gtdbtk_Campylobacter_D.csv'
output_samples_attributes = 'dataflow/00-meta/campylobacter_sample_attributes.csv'


command = 'esearch -db assembly -q ' + search_term + ' | esummary | xtract -pattern DocumentSummary -element AssemblyAccession,BioSampleAccn > ' + output_acc_sample_mapping
os.system(command)

df_map = pd.read_table(output_acc_sample_mapping, header = None)
df_map.columns = ['accession', 'biosample']

df_selected_genus = pd.read_csv(input_selected_genus)

df_selected_genus_samples = pd.merge(df_selected_genus,df_map,on='accession')

sample_att_dict = dict()

for index, row in df_selected_genus_samples.iterrows():
    sample_id = row['biosample']
    command = 'esearch -db biosample -q ' + sample_id + ' | esummary | xtract -pattern DocumentSummary -element Attribute'

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    sample_att_dict.update({sample_id:out})

df_sample_attributes = pd.DataFrame.from_dict(sample_att_dict, orient="index")
df_sample_attributes.to_csv(output_samples_attributes)
