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

meta = pd.read_csv('dataflow/00-meta/complete_genomes.csv', low_memory=False)
genomes = meta['File'].tolist()

files = [item + "_genomic.fna" for item in genomes]

#for file in files:
#    file_path = 'dataflow/01-nucl/complete_genomes/' + file


os.system("gtdbtk classify_wf --genome_dir dataflow/01-nucl/complete_genomes_mags --out_dir dataflow/02-classification --extension fna --cpus 64")


iqtree -s dataflow/02-classification/gtdbtk.bac120.user_msa_trimmed.fasta -m TEST -bb 1000 -alrt 1000 -nt 70
