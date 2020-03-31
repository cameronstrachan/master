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

files = [f for f in os.listdir('dataflow/01-nucl/complete_genomes/') if f.endswith(".fna")]
sg.concat(inputfolder='dataflow/01-nucl/complete_genomes/', outputpath='dataflow/01-nucl/campylobacter_genomes.fasta', filenames=files)

file_obj = sc.Fasta('campylobacter_genomes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('campylobacter_genomes_db')
file_obj.setOutputLocation('dataflow/02-blast-db/')
file_obj.runmakeblastdb()

file_obj = sc.Fasta('novel_campy16s.fasta', 'dataflow/03-asv-seqs/')
file_obj.setOutputName('novel_campy16s_campylobacter_genomes_mapped')
file_obj.setOutputLocation('dataflow/02-blast/')
file_obj.runblast(max_target_seqs=100, db='campylobacter_genomes_db')
