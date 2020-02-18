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

genomes_df = pd.read_csv('dataflow/00-meta/stewart2019_epsilonproteobacteria.csv', low_memory=False)
genomes = genomes_df['file_unzip'].tolist()
files = [item + "_rename.fasta" for item in genomes]

sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/rumen_campylobacter.fasta', filenames=files)

file = "rumen_campylobacter.fasta"

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')

# set output name, location
outputfilename = file.split(".f")[0] + '.gff3'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-gff3/')

# run prodigal
file_obj.runprodigal(gff3 = True)

os.system("bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/mann2018/11L2_ACAGTG.1.fastq.gz out=dataflow/03-sam/mann2018_rumen_campylobacter_nonSARA1.sam ref=dataflow/01-nucl/rumen_campylobacter.fasta > dataflow/00-logs/mann2018_rumen_campylobacter.log")
os.system("htseq-count -s no -t CDS -i ID --additional-attr=ID dataflow/03-sam/mann2018_rumen_campylobacter_nonSARA1.sam dataflow/01-gff3/rumen_campylobacter.gff3 > dataflow/03-sam/mann2018_rumen_campylobacter_nonSARA1.txt")
