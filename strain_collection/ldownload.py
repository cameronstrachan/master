import os, sys
import subprocess
import pandas as pd

from Bio import Entrez, SeqIO

Entrez.email = 'strachc@gmail.com'

# custom libraries

system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

#accession_list = ["ERX594486", "ERX594491", "ERX594482", "ERX594479", "ERX594481", "ERX594483", "ERX594488", "ERX594493", "ERX594480", "ERX594487", "ERX594489", "ERX594490", "ERX594492", "ERX594494", "ERX594495", "ERX594484", "ERX594485"]

#for acc in accession_list:
#    ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq')


accession_nums = list(range(2774, 3101, 1))
accession_list = ['LN61' + str(x) for x in accession_nums]

#for acc in accession_list:
#    ss.srafastqdownlaod(acc, outputdir='dataflow/01-clone')

file= open('goat_clone_library.fasta', 'w')

for id in accession_list:
    handle = Entrez.efetch(db="nucleotide", id=id, rettype="fasta", retmode="text")
    record = handle.read()
    file.write(record)
