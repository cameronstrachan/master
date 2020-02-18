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

file_obj = sc.Fasta('13506AA-11.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('13506AA-11_oneLine.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.saveonelinefasta(header='none')

blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'
file = 'neubauer2018_wetzels201_99_oneline.fasta'

file_obj = sc.Fasta(file, 'dataflow/03-asv-seqs/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = 'neubauer2018_wetzels201_99_oneline.fasta'

file = '13506AA-11_oneLine.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'sanger_all_map.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 500)

# blast against goat clones

file = 'goat_clone_library.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='nucl')

blastdb = 'goat_clone_library.fasta'

file = '13506AA-11_oneLine.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputLocation(blastdir)

outputfilename = 'sanger_goat_clones_map.txt'
file_obj.setOutputName(outputfilename)
file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=20, evalue=1e-3, num_threads = 6, max_hsps = 500)
