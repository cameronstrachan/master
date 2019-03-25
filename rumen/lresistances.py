# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

runprodigal = input("\n" + "Run prodigal on all Prevotella genomes? (y or n):")

if runprodigal == 'y':

    genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
    genomes_df_rumen = genomes_df[genomes_df['source'] == 'rumen']
    genomes = genomes_df_rumen['BinID'].tolist()
    files1 = [item + "_rename.fasta" for item in genomes]

    genomes_df2 = pd.read_csv('dataflow/00-meta/seshadri2018_prevotella.csv', low_memory=False)
    genomes = genomes_df2['file'].tolist()
    files2 = [item + "_rename.fasta" for item in genomes]

    files = list(set(files1 + files2))

    sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/rumen_prevotella.fasta', filenames=files)

    file = "rumen_prevotella.fasta"

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location

    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/01-prot/')

    file_obj.runprodigal()

file = "card_db.fasta"
indir = 'dataflow/01-prot/'
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='prot')

file = "rumen_prevotella.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "rumen_prevotella_card.txt"
blastdb = "card_db.fasta"

file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=1, evalue=1e-3, num_threads = 60)
