import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg


file = "JQ655275.1.fasta"
blastdbdir = 'dataflow/02-blast-db/'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')


indir = 'dataflow/01-nucl/'
blastdir = 'dataflow/02-blast/'
file = "rumen_genomes.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdir)
outputfilename = "JQ655275_rumen_mapping.txt"
file_obj.setOutputName(outputfilename)

blastdb = "JQ655275.1.fasta"

file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=100, evalue=1e-3, num_threads = 60, max_hsps = 5)
