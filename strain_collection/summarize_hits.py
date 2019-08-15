import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

blastfiles = ['sanger_strain_library_oneLine.fasta']
xmlfiles = [f for f in os.listdir('02-blast') if f.endswith(".xml")]

sg.blastxmltotable(xmlinputfolder='02-blast/', blastinputfolder='01-nucl/',outputpath='03-tables/compiled_nr_blast.txt', xmlfilenames=xmlfiles, blastfilename=blastfiles)
