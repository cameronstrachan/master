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

downloaddata = input("\n" + "Download data from Sandri et al 2018? (y or n):")

if downloaddata == 'y':

    accession_nums = list(range(49, 64, 1))
    accession_list = ['SRR54207' + str(x) for x in accession_nums]

    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/sandri2018')

downloaddata = input("\n" + "Download data from Sandri et al 2018 try2? (y or n):")

if downloaddata == 'y':

    accession_nums = list(range(53, 68, 1))
    accession_list = ['SRX27122' + str(x) for x in accession_nums]

    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/sandri2018')

runprodigal = input("\n" + "Run prodigal on all Prevotella genomes to generate gff3 files? (y or n):")

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
    outputfilename = file.split(".f")[0] + '.gff3'
    file_obj.setOutputName(outputfilename)
    file_obj.setOutputLocation('dataflow/01-prot/genes/')

    # run prodigal
    file_obj.runprodigal(gff3 = True)

    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/01-prot/')

    file_obj.runprodigal()

runbowtie == 'y'

#runbowtie = input("\n" + "Run BBMap on Marre 2017 data against rumen Prevotella? (y or n):")

if runbowtie == 'y':
    os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/marre2017/SRX1585089_pass_1.fastq out=dataflow/03-sam/marre2017_rumen_prevotella.sam ref=dataflow/01-nucl/rumen_prevotella.fasta > dataflow/00-logs/marre2017_rumen_prevotella.log")
    os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/marre2017_rumen_prevotella.sam dataflow/01-prot/genes/rumen_prevotella.gff3 > dataflow/03-sam-counts/marre2017_rumen_prevotella.txt")

#runbowtie = input("\n" + "Run BBMap on Mann 2018 data against rumen Prevotella for single non-SARA sample? (y or n):")

if runbowtie == 'y':
    os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/mann2018/11L2_ACAGTG.1.fastq.gz out=dataflow/03-sam/mann2018_rumen_prevotella_nonSARA1.sam ref=dataflow/01-nucl/rumen_prevotella.fasta > dataflow/00-logs/mann2018_rumen_prevotella.log")
    os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/mann2018_rumen_prevotella_nonSARA1.sam dataflow/01-prot/genes/rumen_prevotella.gff3 > dataflow/03-sam-counts/mann2018_rumen_prevotella_nonSARA1.txt")

#runbowtie = input("\n" + "Run BBMap on Mann 2018 data against rumen Prevotella for single SARA sample? (y or n):")

if runbowtie == 'y':
    os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/mann2018/13L2_AFTTCC.1.fastq.gz out=dataflow/03-sam/mann2018_rumen_prevotella_SARA1.sam ref=dataflow/01-nucl/rumen_prevotella.fasta > dataflow/00-logs/mann2018_rumen_prevotella.log")
    os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/mann2018_rumen_prevotella_SARA1.sam dataflow/01-prot/genes/rumen_prevotella.gff3 > dataflow/03-sam-counts/mann2018_rumen_prevotella_SARA1.txt")

#runbowtie = input("\n" + "Run BBMap on sandri 2018 data (4 fastqs) against rumen Prevotella? (y or n):")

if runbowtie == 'y':
    os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/sandri2018/4forwardread.fasta.gz out=dataflow/03-sam/sandri2018_rumen_prevotella.sam ref=dataflow/01-nucl/rumen_prevotella.fasta > dataflow/00-logs/sandri2018_rumen_prevotella.log")
    os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/sandri2018_rumen_prevotella.sam dataflow/01-prot/genes/rumen_prevotella.gff3 > dataflow/03-sam-counts/sandri2018_rumen_prevotella.txt")


#-qtrim=lr
