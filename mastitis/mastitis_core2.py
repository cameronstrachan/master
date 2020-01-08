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

file = 'mastitis_pathogens.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName('mastitis_pathogens_oneLine.fasta')
file_obj.setOutputLocation('dataflow/01-nucl/')
#file_obj.saveonelinefasta()

file = 'mastitis_pathogens_oneLine.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/01-nucl/')

headers = file_obj.fasta2headermap()
df = pd.DataFrame.from_dict(headers, orient="index")
df['file'] = file
df.to_csv('dataflow/03-tables/' + file.split('.fa')[0] + '.csv')

file = 'mastitis_pathogens_oneLine.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal(type='prot')

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/02-blast-db/')
#file_obj.runmakeblastdb(dbtype='prot')

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputLocation('dataflow/03-tables/')
file_obj.setOutputName('mastitis_core.txt')
file_obj.runblast(blast='blastp', db=file, dblocation='dataflow/02-blast-db/', max_target_seqs=153, evalue=1e-6, num_threads = 4)
