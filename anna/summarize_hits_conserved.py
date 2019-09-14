import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

blastfiles = ['nitrospinae_genomes_above80.fasta']
xmlfiles = [f for f in os.listdir('dataflow/02-blast/conserved80/') if f.endswith(".xml")]

sg.blastxmltotable(xmlinputfolder='dataflow/02-blast/conserved80/', blastinputfolder='dataflow/01-prot/',outputpath='dataflow/03-tables/nitrospinae_genomes_above80.txt', xmlfilenames=xmlfiles, blastfilename=blastfiles)
