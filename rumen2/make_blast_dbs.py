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

file_obj = sc.Fasta('listeria_monocytogenes.fasta', '01-nucl/')
file_obj.setOutputName('listeria_monocytogenes.fasta')
file_obj.setOutputLocation('02-blast-db/')
file_obj.runmakeblastdb(dbtype='nucl')

file_obj = sc.Fasta('staphylococcus_aureus.fasta', '01-nucl/')
file_obj.setOutputName('staphylococcus_aureus.fasta')
file_obj.setOutputLocation('02-blast-db/')
file_obj.runmakeblastdb(dbtype='nucl')

file_obj = sc.Fasta('campylobacter_coli.fasta', '01-nucl/')
file_obj.setOutputName('campylobacter_coli.fasta')
file_obj.setOutputLocation('02-blast-db/')
file_obj.runmakeblastdb(dbtype='nucl')
