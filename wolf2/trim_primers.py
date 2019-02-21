import os, sys

forward = input('\n' + 'Input forward primer sequence:')

forward_in = ' -g ' + str(forward) + ' '

reverse = input('\n' + 'Input reverse primer sequence:')

reverse_in = ' -g ' + str(reverse) + ' '

dirin = 'dataflow/01-fastq/'
dirout = 'dataflow/01-fastq/trimmed/'

files = [f for f in os.listdir(dirin) if f.endswith('.fastq.gz')]

for file in files:
	type = file.split('_')[3]
	input = dirin + file
	output = dirout + file
	
	if type == 'R1':
		command = 'cutadapt  -f "fastq"  -o ' + output + forward_in + input
	else:
		command = 'cutadapt  -f "fastq"  -o ' + output + reverse_in + input

	os.system(command)

