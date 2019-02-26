import os, sys

print("\n" + 'This is a qimme2 wrapper to standaridize running qimme2')

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

if os.path.exists('dataflow/00-databases') == False:
	os.mkdir('dataflow/00-databases')

check = input("\n" + "Ensure that zipped demultiplexed data is in dataflow/00-fastq with the illumina naming (ex. SampleName_SampleNumber_L001_R1_001.fastq.gz) then hit enter:")
check = input("\n" + "Ensure that sample-metadata.tsv is in dataflow/00-meta in the qimme2 format and hit enter:")
check = input("\n" + "Ensure silva database files are in 00-databases (silva_132_99_16S.fna and taxonomy_7_levels.txt):")

dirs = ['02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']
#dirs_control = [d + '-control' for d in dirs]

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)


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

	if paired == True:

		type = file.split('_')[3]
		input_f = dirin + file
		output_f = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output_f + forward_in + input_f + ' > 00-logs/forward_primer_trimming_stats.txt'
		else:
			command = 'cutadapt  -f "fastq"  -o ' + output_f + reverse_in + input_f + ' > 00-logs/reverse_primer_trimming_stats.txt'

		os.system(command)

	else:

		# Need to check this is the correct way to trim non-paired reads

		type = file.split('_')[3]
		input_f = dirin + file
		output_f = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output_f + forward_in + input_f + ' > 00-logs/forward_primer_trimming_stats.txt'
			command = 'cutadapt  -f "fastq"  -o ' + output_f + reverse_in + output_f + ' > 00-logs/reverse_primer_trimming_stats.txt'


		os.system(command)

retrain = input('\n' + 'Re-train classifier with primer set? (y or n):')

if retrain == 'y':

	command = 'bash/q2pipeline/q2_train-classifier.sh ' + str(forward) + ' ' + str(reverse)

	os.system(command)


print('\n' + 'DATA IMPORT' + '\n')

if paired == True:
	os.system('bash/q2pipeline/q2_import.sh \'SampleData[PairedEndSequencesWithQuality]\'')

else:
	os.system('bash/q2pipeline/q2_import.sh \'SampleData[SequencesWithQuality]\'')


print('\n' + 'Visualize dataflow/02-qiime-viz/demux-trimmed.qzv at https://view.qiime2.org/' + '\n')

print('\n' + 'DADA2' + '\n')

cores = str(input('\n' + 'Number of cores to use with DADA2 (interger):'))

if paired == True:

	left_forward = str(input("\n" + "Forward Read, Left Cutoff? (interger):"))

	left_reverse = str(input("\n" + "Reverse Read, Left Cutoff? (interger):"))

	trunc_forward = str(input("\n" + "Forward Read, Length Cutoff? (interger):"))

	trunc_reverse = str(input("\n" + "Reverse Read, Length Cutoff? (interger):"))

	command = 'bash/q2pipeline/q2_dada2-paired.sh ' + left_forward + ' ' + left_reverse + ' ' + trunc_forward + ' ' + trunc_reverse + ' ' + cores

	os.system(command)

else:

	left = str(input("\n" + "Left Cutoff? (interger):"))

	trunc = str(input("\n" + "Length Cutoff? (interger):"))

	command = 'bash/q2pipeline/q2_dada2-single.sh ' + left + ' ' + trunc + ' ' + cores

	os.system(command)

print('\n' + '97% Clustering' + '\n')

os.system('bash/q2pipeline/q2_clustering97.sh')

print('\n' + 'Classification' + '\n')

os.system('bash/q2pipeline/q2_classify.sh')

print('\n' + 'Core Metrics' + '\n')

os.system('bash/q2pipeline/q2_core_metrics.sh')
