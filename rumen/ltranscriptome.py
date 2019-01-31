# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

downloaddata = input("\n" + "Download data from Marre et al 2017? (y or n):")

if downloaddata == 'y':
    ss.srafastqdownlaod('SRX1585089', outputdir='dataflow/01-fastq/marre2017')

runprodigal = input("\n" + "Run prodigal on all Prevotella genomes to generate gff3 files? (y or n):")

if runprodigal == 'y':

	genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
	genomes_df_rumen = genomes_df[genomes_df['source'] == 'rumen']
	genomes = genomes_df_rumen['BinID'].tolist()
	files = [item + "_rename.fasta" for item in genomes]
    
    sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/rumen_prevotella.fasta', filenames=files)

    file = "rumen_prevotella.fasta"

	file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
	# set output name, location
	outputfilename = file.split(".f")[0] + '.gff3'
	file_obj.setOutputName(outputfilename)
	file_obj.setOutputLocation('dataflow/01-prot/genes/')

	# run prodigal
	file_obj.runprodigal(gff3 = True)

runbowtie = input("\n" + "Run bowtie on rumen_prevotella.fasta? (y or n):")

if runbowtie == 'y':

    os.system("bowtie2-build —threads 8 dataflow/01-nucl/rumen_prevotella.fasta dataflow/03-bowtie/rumen_prevotella")
    os.system("bowtie2 -p 40 --trim5 10 --trim3 10 --very-sensitive-local --local -x dataflow/03-bowtie/rumen_prevotella -1 dataflow/01-fastq/marre2017/SRX1585089_pass_1.fastq -2 dataflow/01-fastq/marre2017/SRX1585089_pass_2.fastq -S dataflow/03-bowtie/rumen_prevotella.sam")
