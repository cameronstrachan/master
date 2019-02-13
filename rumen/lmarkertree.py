# python libraries
import os, sys
import subprocess
import pandas as pd

#custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

runprodigal = input("\n" + "Run prodigal on all Prevotella genomes to generate prot file? (y or n):")

if runprodigal == 'y':

    genomes_df = pd.read_csv('dataflow/00-meta/checkM_summary_clean_prevotella.csv', low_memory=False)
    genomes_df_rumen = genomes_df[genomes_df['source'] == 'rumen']
    genomes = genomes_df_rumen['BinID'].tolist()
    files = [item + "_rename.fasta" for item in genomes]



    sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/rumen_prevotella.fasta', filenames=files)

    file = "rumen_prevotella.fasta"

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
    file_obj.setOutputName(file )
    file_obj.setOutputLocation('dataflow/01-prot/')

    # run prodigal
    file_obj.runprodigal()

runhmm = input("\n" + "Run hmmer for hsp70? (y or n):")

if runhmm == 'y':
    os.system("hmmpress dataflow/02-hmm/HSP70.hmm")
    os.system("hmmscan --tblout dataflow/02-hmm/rumen_prevotella_hsp70.txt -T 200 --cpu 60 dataflow/02-hmm/HSP70.hmm dataflow/01-prot/rumen_prevotella.fasta")

    hsp70_df = pd.read_csv('dataflow/02-hmm/rumen_prevotella_hsp70.txt', comment='#', header=None, delim_whitespace=True)
    hsp70_genes = hsp70_df.iloc[:,2].tolist()

    file_obj = sc.Fasta('rumen_prevotella.fasta', 'dataflow/01-prot/')
    file_obj.setOutputName('rumen_prevotella_hsp70.fasta')
    file_obj.setOutputLocation('dataflow/01-prot/')
    file_obj.subsetfasta(seqlist = hsp70_genes, headertag='hsp70')

    file_obj = sc.Fasta('rumen_prevotella_hsp70.fasta', 'dataflow/01-prot/')
    file_obj.setOutputName('rumen_prevotella_hsp70_500.fasta')
    file_obj.setOutputLocation('dataflow/01-prot/')
    file_obj.lengthcutoff(replaceheaders = False, length = 500)

runhmm = input("\n" + "Run hmmer for EF-tu? (y or n):")

if runhmm == 'y':
    os.system("hmmpress dataflow/02-hmm/GTP_EFTU.hmm")
    os.system("hmmscan --tblout dataflow/02-hmm/rumen_prevotella_EFTU.txt -T 200 --cpu 60 dataflow/02-hmm/GTP_EFTU.hmm dataflow/01-prot/rumen_prevotella.fasta")

    eftu_df = pd.read_csv('dataflow/02-hmm/rumen_prevotella_EFTU.txt', comment='#', header=None, delim_whitespace=True)
    eftu_genes = eftu_df.iloc[:,2].tolist()

    file_obj = sc.Fasta('rumen_prevotella.fasta', 'dataflow/01-prot/')
    file_obj.setOutputName('rumen_prevotella_EFTU.fasta')
    file_obj.setOutputLocation('dataflow/01-prot/')
    file_obj.subsetfasta(seqlist = eftu_genes, headertag='EFTU')

    #file_obj = sc.Fasta('rumen_prevotella_EFTU.fasta', 'dataflow/01-prot/')
    #file_obj.setOutputName('rumen_prevotella_EFTU_500.fasta')
    #file_obj.setOutputLocation('dataflow/01-prot/')
    #file_obj.lengthcutoff(replaceheaders = False, length = 500)


#hmmpress dataflow/02-hmm/HSP70.hmm
#hmmscan --tblout dataflow/02-hmm/out.test -T 200 --cpu 60 dataflow/02-hmm/HSP70.hmm dataflow/01-prot/rumen_prevotella.fasta
