import os, sys

input_file = 'dataflow/01-nucl/selected_genomes/'
output_file = 'dataflow/02-ani/'

files = [f for f in os.listdir('dataflow/01-nucl/selected_genomes/') if f.endswith(".fna")]


for file in files:
  file1 = input_file + file
  file1_name = file.split('.fn')[0]
  for file in files:
    file2 = input_file + file
    file2_name = file.split('.fn')[0]

    output = output_file + file1_name + '_' + file2_name
    command = 'fastANI -t 40 -q ' + file1 + ' -r ' + file2 + ' -o ' + output

#command = 'cat *.txt > compiled.txt'
#os.system(command)
