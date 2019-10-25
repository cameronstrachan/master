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

file_obj = sc.Fasta('epithelial_cultured_strains.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('epithelial_cultured_strains_oneLine.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.saveonelinefasta()

blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta('neubauer2018_wetzels201_99_oneline.fasta', 'dataflow/03-asv-seqs/')
file_obj.setOutputName('neubauer2018_wetzels201_99_oneline.fasta')
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = 'neubauer2018_wetzels201_99_oneline.fasta'

file_obj = sc.Fasta('epithelial_cultured_strains_oneLine.fasta', 'dataflow/01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'sanger_epithelial_cultured_strains_to_baseline.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 20)

file_obj = sc.Fasta('core_epithelial_microbiome_99_oneline.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('core_epithelial_microbiome_99_oneline.fasta')
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = 'core_epithelial_microbiome_99_oneline.fasta'

file_obj = sc.Fasta('epithelial_cultured_strains_oneLine.fasta', 'dataflow/01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'sanger_epithelial_cultured_strains_to_core.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 20)
