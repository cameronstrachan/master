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
ap.add_argument("-o", "--output_folder", required=True,
   help="output folder, ex. 'output/")
ap.add_argument("-e", "--file_extension", required=True,
   help="extension for the genome files, ex. '.fasta'")
ap.add_argument("-t", "--threads", required=True,
   help="number of threads to use.")

args = vars(ap.parse_args())

# User defined arguments
input_folder = str(args['input_folder'])
output_folder = str(args['output_folder'])
genome_extension = str(args['file_extension'])
threads = int(args['threads'])

# Outputs
output_file_ani = output_folder + 'ani_output.csv'
output_file_regions = output_folder + 'conserved_regions_output.csv'
output_file_map = output_folder + 'frament_map.csv'

# Hardcoded parameters
fragment_step = 500
fragment_length = 1000
decimals = 1
dist = 5
cont = 10

# List of final dataframes
dataframes_list = list()
dataframes_map_list = list()

# Set up temporary folders
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
    genome1_obj.split_up_genome(fragment_size=fragment_length, step=fragment_step, write_to='multiple')
    df_fragment_map = genome1_obj.split_up_genome_map(fragment_size=fragment_length, step=fragment_step)
    df_fragment_map['genome1'] = input_file_name
    df_fragment_map_colrename = df_fragment_map[["genome1", 'header', 'contig', 'fragment_num', 'start', 'stop', 'fragment_size', 'fragment_step']]

    # list of fragmented genomes
    fragment_file_list = [f for f in os.listdir(temp_folder_fragments) if f.endswith(".fasta")]
    fragment_file_list_file = temp_folder + 'genome_fragments.txt'

    fa.savefiles2list(fragment_file_list, temp_folder_fragments, fragment_file_list_file)

    # run fastani
    df_fragment_output = fa.allvall_fastani(fragment_file_list_file, genome_file_list_file, threads=threads, fragment_length=fragment_length, extension=genome_extension)

    # clean up output
    df_fragment_output['genome1'] = input_file_name
    df_fragment_output['fragment_size'] = fragment_length
    df_fragment_output['fragment_step'] = fragment_step
    df_fragment_output["seq1"] = pd.to_numeric(df_fragment_output["seq1"])

    # save output

    df_final_output_genome = pd.merge(left=df_output, right=df_fragment_output, on=["genome1", "seq2"])
    df_final_output_genome_sort = df_final_output_genome.sort_values(by=['seq1'])
    df_final_output_genome_colrename = df_final_output_genome_sort[["genome1", "seq1", "fragment_size", "seq2", "ani", "genome_wide_ani"]]
    df_final_output_genome_colrename.rename(columns={'seq1': 'fragment1', 'fragment_size': 'fragment_size1', 'fragment_step': 'fragment_step1', 'seq2': 'genome2','ani': 'fragment_ani'}, inplace=True)

    dataframes_map_list.append(df_fragment_map_colrename)
    dataframes_list.append(df_final_output_genome_colrename)


df_compiled_ani = pd.concat(dataframes_list)
df_compiled_fragment_map = pd.concat(dataframes_map_list)

### Get continous conserved regions

df_snp = cx.calculate_snp_decrease_df(df_compiled_ani, dec_places = decimals)
df_compiled_regions = cx.extract_continuous_regions(df_snp, distance = dist, n_continuous = cont)

### Save files

df_compiled_ani.to_csv(output_file_ani, index=False)
df_compiled_regions.to_csv(output_file_regions, index=False)
df_compiled_fragment_map.to_csv(output_file_map, index=False)

# clean up
for folder in temp_folders:
    shutil.rmtree(folder)
