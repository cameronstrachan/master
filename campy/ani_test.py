import os, sys

input_file = 'dataflow/01-nucl/selected_genomes/'
output_file = 'dataflow/02-ani/'

files = [f for f in os.listdir('dataflow/01-nucl/selected_genomes/') if f.endswith(".fna")]

with open('dataflow/genomes_list.txt', 'w') as f:
    for file in files:
        f.write("%s\n" % file)

for file in files:
  file1 = input_file + file
  file1_name = file.split('.fn')[0]
  output = output_file + file1_name + '.txt'
  command = 'fastANI -t 70 -q ' + file1_name + ' --rl ' + 'dataflow/genomes_list.txt' + ' -o ' + output
  os.system(command)

os.remove('dataflow/genomes_list.txt')

#command = 'cat *.txt > compiled.txt'
#os.system(command)
