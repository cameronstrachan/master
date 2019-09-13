import os, sys
import pandas as pd

# colours
CRED = '\033[91m'
CGREEN  = '\33[32m'
CEND = '\033[0m'

# two cut offs are hardcoded currently, the sampling depth and the lengths for extracting reads from silva
# need to check the cut adapt parameters for the non paired

# STEP 1. Make directories and print start message.

print("\n" + CRED + 'This is a qimme2 wrapper to standardize running qimme2' + CEND)

if str(sys.argv[1]) == 'single':
	print('\n' + 'Processing single end data')
	paired = False
elif str(sys.argv[1]) == 'paired':
	print('\n' + 'Processing paired end data')
	paired = True

if os.path.exists('dataflow') == False:
	os.mkdir('dataflow')

if os.path.exists('dataflow/00-meta') == False:
	os.mkdir('dataflow/00-meta')

if os.path.exists('dataflow/01-fastq') == False:
	os.mkdir('dataflow/01-fastq')

if os.path.exists('dataflow/01-fastq/trimmed') == False:
	os.mkdir('dataflow/01-fastq/trimmed')

if os.path.exists('dataflow/01-fastq/temp') == False:
	os.mkdir('dataflow/01-fastq/temp')

start_message = 'The zipped and demultiplexed sequencing data must be in dataflow/00-fastq/ with the illumina naming (ex. SampleName_SampleNumber_L001_R1_001.fastq.gz).'

check = input("\n" + start_message + '\n' + '\n' + 'Hit any key to continue')

dirs = ['02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']
#dirs_control = [d + '-control' for d in dirs]

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

# STEP 2. Trim the primers.

print('\n' + CRED + 'PRIMER TRIMMING' + CEND)

forward = input('\n' + 'Forward primer sequence:')

forward_in =  str(forward) + ' '

reverse = input('\n' + 'Reverse primer sequence:')

reverse_in = str(reverse) + ' '

dirin = 'dataflow/01-fastq/'
dirout = 'dataflow/01-fastq/trimmed/'

files = [f for f in os.listdir(dirin) if f.endswith('.fastq.gz')]

for file in files:

	if paired == True:

		type = file.split('_')[3]
		input_f = dirin + file
		output_f = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output_f + ' -g ' + forward_in + input_f + ' >> dataflow/00-logs/forward_primer_trimming_stats.txt'
		else:
			command = 'cutadapt  -f "fastq"  -o ' + output_f + ' -g ' + reverse_in + input_f + ' >> dataflow/00-logs/reverse_primer_trimming_stats.txt'

		os.system(command)

	else:

		type = file.split('_')[3]
		input_f = dirin + file
		output_f_temp = 'dataflow/01-fastq/temp/' + file
		output_f = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output_f_temp + ' -g ' + forward_in + input_f + ' >> dataflow/00-logs/forward_primer_trimming_stats.txt'
			os.system(command)
			command = 'cutadapt  -f "fastq"  -o ' + output_f + ' -g ' + reverse_in + output_f_temp + ' >> dataflow/00-logs/reverse_primer_trimming_stats.txt'
			os.system(command)


# STEP 3. Run DADA2.

print('\n' + CRED + 'DATA IMPORT' + CEND + '\n')

if paired == True:
	os.system('q2pipeline/q2_import.sh \'SampleData[PairedEndSequencesWithQuality]\'')
else:
	os.system('../bash/q2pipeline/q2_import.sh \'SampleData[SequencesWithQuality]\'')

print('\n' + CGREEN + 'Visualize dataflow/02-qiime-viz/demux-trimmed.qzv at https://view.qiime2.org/' + CEND + '\n')

print('\n' + CRED + 'DADA2' + CEND + '\n')

cores = str(input('\n' + 'Number of cores to use with DADA2 (interger):'))

if paired == True:

	left_forward = str(input("\n" + "Forward Read, Left Cutoff? (interger):"))

	left_reverse = str(input("\n" + "Reverse Read, Left Cutoff? (interger):"))

	trunc_forward = str(input("\n" + "Forward Read, Length Cutoff? (interger):"))

	trunc_reverse = str(input("\n" + "Reverse Read, Length Cutoff? (interger):"))

	command = '../bash/q2pipeline/q2_dada2-paired.sh ' + left_forward + ' ' + left_reverse + ' ' + trunc_forward + ' ' + trunc_reverse + ' ' + cores
	print('\n')
	#os.system(command)

	data_params = {'Forward Read, Left Cutoff':left_forward,'Reverse Read, Left Cutoff':left_reverse, "Forward Read, Length Cutoff":trunc_forward, "Reverse Read, Length Cutoff":trunc_reverse}

else:

	left = str(input("\n" + "Left Cutoff? (interger):"))

	trunc = str(input("\n" + "Length Cutoff? (interger):"))

	command = '../bash/q2pipeline/q2_dada2-single.sh ' + left + ' ' + trunc + ' ' + cores
	print('\n')
	os.system(command)

	data_params = {'Left Cutoff':left,'Length Cutoff':trunc}

# STEP 4. Cluster sequences at 97% identity.

print('\n' + CRED + '99% CLUSTERING' + CEND + '\n')

os.system('../bash/q2pipeline/q2_clustering99.sh')
