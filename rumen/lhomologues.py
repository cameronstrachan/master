import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

runcommand = input("\n" + "Run RBH analaysis to export shared homolgoues? (y or n):")

if runcommand == 'y':
	os.system("Rscript src/R/extract_RBH_sharedPI_highlyconserved.R")

runcommand = input("\n" + "Create a fasta with just the homologies? (y or n):")

if runcommand == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
	genomes_df_rumen = genomes_df[genomes_df['source'] == 'rumen']
	genomes = genomes_df_rumen['BinID'].tolist()
	files = [item + "_rename.fasta" for item in genomes]

	sg.concat(inputfolder='dataflow/01-prot/', outputpath='dataflow/01-prot/rumen_prevotella.fasta', filenames=files)

	genes_df = pd.read_csv('dataflow/00-meta/df_conserved_homologues.csv', low_memory=False)
	genes = genes_df['sseqid'].tolist()

	file_obj = sc.Fasta('rumen_prevotella.fasta', 'dataflow/01-prot/')
	file_obj.setOutputName('rumen_prevotella_homologues.fasta')
	file_obj.setOutputLocation('dataflow/01-prot/')
	file_obj.subsetfasta(seqlist = genes, headertag='homologues')

runcommand = input("\n" + "Create a nucl fasta with just the homologies? (y or n):")

if runcommand == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
	genomes_df_rumen = genomes_df[genomes_df['source'] == 'rumen']
	genomes = genomes_df_rumen['BinID'].tolist()
	files = [item + "_rename.fasta" for item in genomes]

	sg.concat(inputfolder='dataflow/01-prot/genes/', outputpath='dataflow/01-prot/genes/rumen_prevotella.fasta', filenames=files)

	genes_df = pd.read_csv('dataflow/00-meta/df_conserved_homologues.csv', low_memory=False)
	genes = genes_df['sseqid'].tolist()

	file_obj = sc.Fasta('rumen_prevotella.fasta', 'dataflow/01-prot/genes/')
	file_obj.setOutputName('rumen_prevotella_homologues.fasta')
	file_obj.setOutputLocation('dataflow/01-prot/genes/')
	file_obj.subsetfasta(seqlist = genes, headertag='homologues')
