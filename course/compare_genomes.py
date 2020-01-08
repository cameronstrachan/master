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

files = ['Prevotella_ruminicola_strain_ATCC19189.fna', \
'Prevotella_ruminicola_strain_D31d.fna']

for file in files:

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    outfilename = file.split('.f')[0] + '_oneLine.fna'
    file_obj.setOutputName(outfilename)
    file_obj.setOutputLocation('dataflow/01-nucl/')
    file_obj.saveonelinefasta()

files = ['Prevotella_ruminicola_strain_ATCC19189_oneLine.fna', \
'Prevotella_ruminicola_strain_D31d_oneLine.fna']

for file in files:
    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    outfilename = file.split('.f')[0] + '.faa'
    file_obj.setOutputName(outfilename)
    file_obj.setOutputLocation('dataflow/02-prot/')
    file_obj.runprodigal(type='prot')

db = 'Prevotella_ruminicola_strain_ATCC19189_oneLine.faa'

file_obj = sc.Fasta(db, 'dataflow/02-prot/')
file_obj.setOutputName(db)
file_obj.setOutputLocation('dataflow/03-blast-db/')
file_obj.runmakeblastdb(dbtype='prot')

file = 'Prevotella_ruminicola_strain_D31d_oneLine.faa'

file_obj = sc.Fasta(file, 'dataflow/02-prot/')
file_obj.setOutputLocation('dataflow/04-tables/')
file_obj.setOutputName('prevotella_comparison.txt')
file_obj.runblast(blast='blastp', db=db, dblocation='dataflow/03-blast-db/', \
max_target_seqs=1, evalue=1e-3, num_threads = 4)
