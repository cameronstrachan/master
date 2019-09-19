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


blastxml = 'dataflow_test/02-blast-xml/'
blastin = 'dataflow_test/01-nucl/'
prot_dir = 'dataflow_test/01-prot/'

file_obj = sc.Fasta('stewart2019_mags_genes_sub_pathogen_mapped.fasta', prot_dir)
file_obj.setOutputLocation(blastxml)
file_obj.runonlineblast(numhits=1)

blastfiles = 'stewart2019_mags_genes_sub_pathogen_mapped.fasta'
xmlfiles = [f for f in os.listdir(blastxml) if f.endswith(".xml")]
sg.blastxmltotable(xmlinputfolder=blastxml, blastinputfolder=blastin,outputpath='dataflow/03-analysis/compiled_annotations.txt', xmlfilenames=xmlfiles, blastfilename=blastfiles)
