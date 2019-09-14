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

# vicki, cow

blastdbdir = '02-blast-db/'
blastdir = '02-blast/'
file = 'neubauer_et_al_epithelial.fasta'

file_obj = sc.Fasta(file, '01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = file

file = 'sanger_strain_library_oneLine.fasta'

file_obj = sc.Fasta(file, '01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'strains_to_neubauer.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 20)

# peffi, cow

blastdbdir = '02-blast-db/'
blastdir = '02-blast/'
file = 'wetzels_et_al.fasta'

file_obj = sc.Fasta(file, '01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = file

file = 'sanger_strain_library_oneLine.fasta'

file_obj = sc.Fasta(file, '01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'strains_to_wetzels.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 20)

# peffi, goat

blastdbdir = '02-blast-db/'
blastdir = '02-blast/'
file = 'wetzels_et_al_goat.fasta'

file_obj = sc.Fasta(file, '01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = file

file = 'sanger_strain_library_oneLine.fasta'

file_obj = sc.Fasta(file, '01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'strains_to_wetzels_goat.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 20)
