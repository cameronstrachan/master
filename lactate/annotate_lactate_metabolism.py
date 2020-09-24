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

files = [f for f in os.listdir('dataflow/01-nucl/') if f.endswith(".fasta")]

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    outputfilename = file.split(".f")[0] + '.fasta'
    file_obj.setOutputName(outputfilename)
    file_obj.setOutputLocation('dataflow/01-prot/')
    file_obj.runprodigal()

dbfiles = ['characterized_lactate_permease.fasta', 'characterized_lactate_production.fasta', 'characterized_lactate_utilization.fasta']

for file in dbfiles:
    file_obj = sc.Fasta(file, 'dataflow/01-prot/')
    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/02-blastdbs/')
    file_obj.runmakeblastdb(dbtype='prot')

blastdbs = ['characterized_lactate_permease.fasta', 'characterized_lactate_production.fasta', 'characterized_lactate_utilization.fasta']

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-prot/')
    file_obj.setOutputLocation('dataflow/03-blastout/')
    for blastdb in blastdbs:
    	outputfilename = file.split('.f')[0] + ':' + blastdb.split('.f')[0] + '.txt'
    	file_obj.setOutputName(outputfilename)
    	file_obj.runblast(blast='blastp', db=blastdb, dblocation='dataflow/02-blastdbs/', max_target_seqs=100, evalue=1e-5, num_threads = 15)

os.system('find dataflow/03-blastout/ -size  0 -print -delete')

hitfiles = [f for f in os.listdir('dataflow/03-blastout/') if f.endswith(".txt")]
df_list = list()

for file in hitfiles:

    genome_file = file.split(':')[0] + '.fasta'
    file_loc = 'dataflow/03-blastout/' + file
    df_file = pd.read_csv(file_loc, sep = '\t', low_memory=False, header=None)
    orfs = list(set(df_file.iloc[:,0].tolist()))

    category_file = file.split(':')[1].split('.txt')[0]
    category = file.split(':')[1].split('.txt')[0].split('lactate_')[1]
    subset_file = genome_file.split('.fa')[0] + ':' + category_file + '.fasta'

    file_obj = sc.Fasta(genome_file, 'dataflow/01-prot/')
    file_obj.setOutputName(subset_file)
    file_obj.setOutputLocation('dataflow/01-prot/selected/')
    file_obj.subsetfasta(seqlist=orfs, headertag=category)

    file_obj = sc.Fasta(genome_file, 'dataflow/01-prot/')
    file_obj.setOutputName(genome_file)
    headers = file_obj.fasta2headermap()
    df = pd.DataFrame.from_dict(headers, orient="index")
    df['file'] = genome_file
    df['category'] = category

    df = df[df.loc[:].isin(orfs)]
    df_list.append(df)

df_headers = pd.concat(df_list)
df_headers.to_csv('dataflow/00-meta/selected_prot_headers.csv')
