import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

blastfiles = ['extracted_regions_oneLine.fasta']
xmlfiles = [f for f in os.listdir('dataflow/02-blast') if f.endswith(".xml")]

sg.blastxmltotable(xmlinputfolder='dataflow/02-blast/', blastinputfolder='dataflow/01-prot/',outputpath='dataflow/03-tables/compiled_nr_blast.txt', xmlfilenames=xmlfiles, blastfilename=blastfiles)
