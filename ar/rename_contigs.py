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

pathogen_folders = ['staphylococcus aureus', 'campylobacter coli', 'campylobacter jejuni', 'clostridioides difficile', 'salmonella typhimurium', 'salmonella newport']

runprodigal = input("\n" + "Rename pathogen genomes? (y or n):")

if runprodigal == 'y':

    for pathogen_folder in pathogen_folders:

        genomes_input_folder = 'dataflow/01-dbs/' + pathogen_folder
        genome_extension = '.fna.gz'

        genome_files_zip = [f for f in os.listdir(genomes_input_folder) if f.endswith(genome_extension)]

        for file_zip in genome_files_zip:

            os.system('gunzip ' + file_zip)

            file = file_zip.split('.gz')[0]

            file_obj = sc.Fasta(file, genomes_input_folder)
            output_name = file.split('.fna')[0] + '_rename.fasta'
            file_obj.setOutputName(output_name)
            file_obj.setOutputLocation(genomes_input_folder)
            file_obj.headerrename()

            file_to_remove = genomes_input_folder + file

            os.remove(file_to_remove)
