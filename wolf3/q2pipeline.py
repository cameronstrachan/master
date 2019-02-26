import os, sys

runpipeline = input("\n" + "Would you like to run the qiime2 pipeline? This will make a dataflow directory with several subdirectories. (y or n):")

if runpipeline != 'y':
	sys.exit()

print("\n" + 'This is a qimme2 wrapper to standaridize running qimme2. Add -h for more info.')

if os.path.exists('dataflow') == False:
	os.mkdir('dataflow')

if os.path.exists('dataflow/00-meta') == False:
	os.mkdir('dataflow/00-meta')

if os.path.exists('dataflow/01-fastq') == False:
	os.mkdir('dataflow/01-fastq')

if os.path.exists('dataflow/01-fastq/trimmed') == False:
	os.mkdir('dataflow/01-fastq/trimmed')

check = input("\n" + "Ensure that zipped demultiplexed data is in dataflow/00-fastq with the illumina naming format (ex. SampleName_SampleNumber_L001_R1_001.fastq.gz) then hit enter:" + '\n')
check = input("\n" + "Ensure that meta data file (.tsv) is in dataflow/00-meta as a tsv in qimme2 format and hit enter:" + '\n')


dirs = ['02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table']
#dirs_control = [d + '-control' for d in dirs]

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

paired = input("\n" + 'Are you working with paired end data (all files contain R1)? (y or n):')

print('\n' + 'PRIMER TRIMMING' + '\n')

forward = input('\n' + 'Input forward primer sequence:')

forward_in = ' -g ' + str(forward) + ' '

reverse = input('\n' + 'Input reverse primer sequence:')

reverse_in = ' -g ' + str(reverse) + ' '

print('\n')

dirin = 'dataflow/01-fastq/'
dirout = 'dataflow/01-fastq/trimmed/'

files = [f for f in os.listdir(dirin) if f.endswith('.fastq.gz')]

for file in files:

	if paired == 'y':

		type = file.split('_')[3]
		input = dirin + file
		output = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output + forward_in + input
		else:
			command = 'cutadapt  -f "fastq"  -o ' + output + reverse_in + input

		os.system(command)

	else:

		# Need to check this is the correct way to trim non-paired reads

		type = file.split('_')[3]
		input = dirin + file
		output = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output + forward_in + input
			command = 'cutadapt  -f "fastq"  -o ' + output + reverse_in + output


		os.system(command)


print('\n' + 'DATA IMPORT' + '\n')

if paired == 'y':
	os.system('bash/q2pipeline/q2_import.sh \'SampleData[PairedEndSequencesWithQuality]\'')

else:
	os.system('bash/q2pipeline/q2_import.sh \'SampleData[SequencesWithQuality]\'')


print('\n' + 'Visualize dataflow/02-qiime-viz/demux-paired-end.qzv at https://view.qiime2.org/' + '\n')

print('\n' + 'DADA2' + '\n')

cores = input("\n" + "Number of threads? (interger):")

if paired == 'y':

	left_forward = input("\n" + "Forward Read, Left Cutoff? (interger):")

	left_reverse = input("\n" + "Reverse Read, Left Cutoff? (interger):")

	trunc_forward = input("\n" + "Forward Read, Length Cutoff? (interger):")

	trunc_reverse = input("\n" + "Reverse Read, Length Cutoff? (interger):")

	command = 'bash/q2pipeline/q2_data2-paired.sh ' + left_forward + ' ' + left_reverse + ' ' + trunc_forward + ' ' + trunc_reverse + ' ' + cores

	os.system(command)

else:

	left = input("\n" + "Left Cutoff? (interger):")

	trunc = input("\n" + "Length Cutoff? (interger):")

	command = 'bash/q2pipeline/q2_data2-single.sh ' + left + ' ' + trunc + ' ' + cores

	os.system(command)
