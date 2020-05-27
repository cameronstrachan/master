# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/ar/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/ar/')

from modules import seq_core as sc


def concat(inputfolder='path/to/input/', outputpath='path/to/output/file.txt', filenames=[]):

	if not os.path.exists(outputpath):
		with open(outputpath, 'w') as outfile:
		    for file in filenames:
		        with open(inputfolder + file) as infile:
		            for line in infile:
		                outfile.write(line)
	else:
		print("\n" + 'File already exists: ' + outputpath)


pathogen_folders = ['staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis']

genome_extension = '.fasta'

runmakeblastdb = input("\n" + "Make blast databases? (y or n):")

if runmakeblastdb == 'y':

    for pathogen_folder in pathogen_folders:

        input_folder = 'dataflow/01-dbs/pathogens/'
        genomes_input_folder = input_folder + pathogen_folder + '/'
        output_file = input_folder + pathogen_folder + '.fasta'

        genome_files = [f for f in os.listdir(genomes_input_folder) if f.endswith(genome_extension)]

        concat(inputfolder=genomes_input_folder, outputpath=output_file, filenames=genome_files)

        file = pathogen_folder + '.fasta'
        blastdbdir = 'dataflow/01-dbs/blastdbs/'

        file_obj = sc.Fasta(file, input_folder)
        file_obj.setOutputName(pathogen_folder)
        file_obj.setOutputLocation(blastdbdir)
        file_obj.runmakeblastdb(dbtype='nucl')

        file_to_remove = input_folder + file

        os.remove(file_to_remove)
