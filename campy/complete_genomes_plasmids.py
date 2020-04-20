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

genome_length_cutoff = 1000000

df_genomes = pd.read_csv('dataflow/00-meta/gtdbtk_Campylobacter_D.csv', low_memory=False)
contigs = dict()
df_contig_lengths_output = 'dataflow/00-meta/gtdbtk_Campylobacter_D_contig_lengths.csv'

for index, row in df_genomes.iterrows():

    file = row['file']
    acc = row['accession']

    file_major_contig = file.replace('_genomic', '_major_contig')
    file_minor_cotigs = file.replace('_genomic', '_minor_cotigs')

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    file_obj.setOutputLocation('dataflow/01-nucl/selected_genomes/')

    fastadic = file_obj.fasta2dict()

    full_genomes_count = 0

    file_obj.setOutputName(file_major_contig)
    outputfile = file_obj.openwritefile()
    file_obj.setOutputLocation('dataflow/01-nucl/selected_genomes/')

    for k,v in fastadic.items():
        header = k.replace(':', '')
        if len(v) > genome_length_cutoff:
            outputfile.write(">" + header + '_' + str(len(v)) + '\n')
            outputfile.write(v + '\n')
            contig_name = acc + '_' + header
            contigs.update({contig_name:len(v)})
            full_genomes_count = full_genomes_count + 1

    if full_genomes_count == 0:
        file_obj.deleteoutput()

    plasmids_genomes_count = 0

    file_obj.setOutputName(file_minor_cotigs)
    file_obj.setOutputLocation('dataflow/01-nucl/selected_small_contigs/')
    outputfile = file_obj.openwritefile()

    for k,v in fastadic.items():
        if len(v) < genome_length_cutoff:
            outputfile.write(">" + header + '_' + str(len(v)) + '\n')
            outputfile.write(v + '\n')
            contig_name = acc + '_' + header
            contigs.update({contig_name:len(v)})
            plasmids_genomes_count = plasmids_genomes_count + 1

    if plasmids_genomes_count == 0:
        file_obj.deleteoutput()

df_contig_lengths = pd.DataFrame.from_dict(contigs, orient="index")
df_contig_lengths.to_csv(df_contig_lengths_output)
