# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

### MAP TRANSCRIPTOMES
### Environment: source activate anaconda

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

runbowtie = input("\n" + "Run BBMap on Marre 2017 data against rumen Prevotella? (y or n):")

if runbowtie == 'y':
    os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/marre2017/SRX1585089_pass_1.fastq out=dataflow/03-sam/marre2017_rumen_prevotella.sam ref=dataflow/01-nucl/rumen_prevotella.fasta > dataflow/00-logs/marre2017_rumen_prevotella.log")
    os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/marre2017_rumen_prevotella.sam dataflow/01-prot/genes/rumen_prevotella.gff3 > dataflow/03-sam-counts/marre2017_rumen_prevotella.txt")

runbowtie = input("\n" + "Run BBMap on Mann 2018 data against rumen Prevotella? (y or n):")

if runbowtie == 'y':
    os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/mann2018/11L2_ACAGTG.1.fastq.gz out=dataflow/03-sam/mann2018_rumen_prevotella.sam ref=dataflow/01-nucl/rumen_prevotella.fasta > dataflow/00-logs/mann2018_rumen_prevotella.log")
    os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/mann2018_rumen_prevotella.sam dataflow/01-prot/genes/rumen_prevotella.gff3 > dataflow/03-sam-counts/mann2018_rumen_prevotella.txt")
