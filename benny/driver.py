#!/Users/cameronstrachan/anaconda/bin/ python3
# -*- coding: utf-8 -*-

### WRITING A SCRIPT TO ANALYZE INDIVIDUAL FOSMIDS

# python libraries
import os, sys
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg

file_obj = sc.Fasta('Pacbio_dna.fasta', 'dataflow/01-nucl/')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.setOutputName('Pacbio_dna_rename.fasta')
file_obj.headerrename()

file_obj = sc.Fasta('Illumina_dna.fasta', 'dataflow/01-nucl/')
file_obj.setOutputLocation('dataflow/01-nucl/')
file_obj.setOutputName('Illumina_dna_rename.fasta')
file_obj.headerrename()


runmakedb = input("\n" + "Make nucl blast database with fpac bio data? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('Pacbio_dna_rename.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('Pacbio_dna_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()

runblast = input("\n" + "Run blast illumina v pac bio? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('Illumina_dna_rename.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('illumina_v_pacbio')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(db='Pacbio_dna_db')

