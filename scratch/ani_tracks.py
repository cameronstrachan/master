#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import pandas as pd
import shutil
import argparse

sys.path.insert(0, '/Users/cameronstrachan/master/scratch/')
from modules import popani_core as pc
from modules import fastani as fa
from modules import conservX as cx

# construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-i", "--input_folder", required=True,
   help="input folder with genomes, ex. 'genomes/'.")
ap.add_argument("-o", "--output_file", required=True,
   help="location and name for the output file, ex. 'output/fragment_ani_analysis.csv")
ap.add_argument("-f", "--fragment_length", required=True,
   help="value to be used for the fragment length, ex. 3000.")
ap.add_argument("-e", "--file_extension", required=True,
   help="extension for the genome files, ex. '.fasta'")
ap.add_argument("-t", "--threads", required=True,
   help="number of threads to use.")

args = vars(ap.parse_args())

input_folder = str(args['input_folder'])
output_file = str(args['output_file'])
fragment_length = int(args['fragment_length'])
genome_extension = str(args['file_extension'])
threads = int(args['threads'])

output_file_regions = os.path.splitext(output_file)[0] + '_regions.csv'
num_dec = len(str(fragment_length)) - 1

# list of final dataframes
dataframes_list = list()

# set up temporary folders
temp_folder = 'temp/'
temp_folder_fragments = 'temp_fragments/'
temp_folders = [temp_folder, temp_folder_fragments]

for folder in temp_folders:
    if os.path.exists(folder) == False:
    	os.mkdir(folder)
    else:
        shutil.rmtree(folder)
        os.mkdir(folder)

# genomes to work with
genome_file_list = [f for f in os.listdir(input_folder) if f.endswith(genome_extension)]

# make genome list file
genome_file_list_file = temp_folder + 'genomes.txt'
fa.savefiles2list(genome_file_list, input_folder, genome_file_list_file)

### first get genome wide ANI
df_output = fa.allvall_fastani(genome_file_list_file, genome_file_list_file, threads=threads, extension=".fasta")

# modify columns to merge with fragmented files
df_output.rename(columns={'seq1': 'genome1', 'ani': 'genome_wide_ani'}, inplace=True)

### run ANI across fragments
# input genomes
for input_file in genome_file_list:

    input_file_name = input_file.split(genome_extension)[0]

    # fragment the input genome
    genome1_obj = pc.Fasta(input_file, input_folder)
    genome1_obj.setOutputLocation(temp_folder_fragments)
    genome1_obj.split_up_genome(fragment_size=fragment_length, write_to='multiple')

    # list of fragmented genomes
    fragment_file_list = [f for f in os.listdir(temp_folder_fragments) if f.endswith(".fasta")]
    fragment_file_list_file = temp_folder + 'genome_fragments.txt'

    fa.savefiles2list(fragment_file_list, temp_folder_fragments, fragment_file_list_file)

    # run fastani
    df_fragment_output = fa.allvall_fastani(fragment_file_list_file, genome_file_list_file, threads=threads, fragment_length=fragment_length, extension=genome_extension)

    # clean up output
    df_fragment_output['genome1'] = input_file_name
    df_fragment_output['fragment_size'] = fragment_length
    df_fragment_output["seq1"] = pd.to_numeric(df_fragment_output["seq1"])

    # save output

    df_final_output_genome = pd.merge(left=df_output, right=df_fragment_output, on=["genome1", "seq2"])
    df_final_output_genome = df_final_output_genome.sort_values(by=['seq1'])
    df_final_output_genome = df_final_output_genome[["genome1", "seq1", "fragment_size", "seq2", "ani", "genome_wide_ani"]]
    df_final_output_genome.rename(columns={'seq1': 'fragment1', 'fragment_size': 'fragment_size1', 'seq2': 'genome2','ani': 'fragment_ani'}, inplace=True)

    dataframes_list.append(df_final_output_genome)


df_final = pd.concat(dataframes_list)

### Export continous regions

df_snp = cx.calculate_snp_decrease_df(df_final, dec_places = num_dec)
df_final_regions = cx.extract_continuous_regions(df_snp, distance = 1)

### Save files

df_final.to_csv(output_file, index=False)
df_final_regions.to_csv(output_file_regions, index=False)

# clean up
for folder in temp_folders:
    shutil.rmtree(folder)
