import os, sys
import pandas as pd

# two cut offs are hardcoded currently, the sampling depth and the lengths for extracting reads from silva
# need to check the cut adapt parameters for the non paired

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

start_message = 'There needs to be several files in the correct directories before running this pipeline. First, the zipped and demultiplexed sequencing data must be in dataflow/00-fastq/ with the illumina naming (ex. SampleName_SampleNumber_L001_R1_001.fastq.gz). If the data is not paired, then every file will contain the R1, which must be after the 3rd underscore. Second, the file sample-meta.tsv must be in dataflow/00-meta/ and formatted as specified by qiime2. Lastly the silva databases that we are currently using must be in dataflow/00-dabases/. There are two files for the silva database, silva_132_99_16S.fna and taxonomy_7_levels.txt.'

check = input("\n" + start_message + '\n' + '\n' + 'Hit any key to continue')

dirs = ['02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']
#dirs_control = [d + '-control' for d in dirs]

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

if os.path.exists('dataflow/02-qiime-viz/beta-sig') == False:
	os.mkdir('dataflow/02-qiime-viz/beta-sig')

print('\n' + 'PRIMER TRIMMING')

forward = input('\n' + 'Forward primer sequence:')

forward_in = ' -g ' + str(forward) + ' '

reverse = input('\n' + 'Reverse primer sequence:')

reverse_in = ' -g ' + str(reverse) + ' '

dirin = 'dataflow/01-fastq/'
dirout = 'dataflow/01-fastq/trimmed/'

files = [f for f in os.listdir(dirin) if f.endswith('.fastq.gz')]

for file in files:

	if paired == True:

		type = file.split('_')[3]
		input_f = dirin + file
		output_f = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output_f + forward_in + input_f + ' > dataflow/00-logs/forward_primer_trimming_stats.txt'
		else:
			command = 'cutadapt  -f "fastq"  -o ' + output_f + reverse_in + input_f + ' > dataflow/00-logs/reverse_primer_trimming_stats.txt'

		os.system(command)

	else:

		# Need to check this is the correct way to trim non-paired reads

		type = file.split('_')[3]
		input_f = dirin + file
		output_f = dirout + file

		if type == 'R1':
			command = 'cutadapt  -f "fastq"  -o ' + output_f + forward_in + input_f + ' > dataflow/00-logs/forward_primer_trimming_stats.txt'
			command = 'cutadapt  -f "fastq"  -o ' + output_f + reverse_in + output_f + ' > dataflow/00-logs/reverse_primer_trimming_stats.txt'


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
	print('\n')
	os.system(command)

	data_params = {'Forward Read, Left Cutoff':left_forward,'Reverse Read, Left Cutoff':left_reverse, "Forward Read, Length Cutoff":trunc_forward, "Reverse Read, Length Cutoff":trunc_reverse}

else:

	left = str(input("\n" + "Left Cutoff? (interger):"))

	trunc = str(input("\n" + "Length Cutoff? (interger):"))

	command = 'bash/q2pipeline/q2_dada2-single.sh ' + left + ' ' + trunc + ' ' + cores
	print('\n')
	os.system(command)

	data_params = {'Left Cutoff':left,'Length Cutoff':trunc}

print('\n' + 'TRAIN CLASSIFIER' + '\n')

minLength = 100
maxLength = 400

command = 'bash/q2pipeline/q2_train_classifier.sh ' + str(forward) + ' ' + str(reverse) + ' ' + str(minLength) + ' ' + str(maxLength)

os.system(command)

print('\n' + '97% Clustering' + '\n')

os.system('bash/q2pipeline/q2_clustering97.sh')

print('\n' + 'Classification' + '\n')

os.system('bash/q2pipeline/q2_classify.sh')

print('\n' + 'Core Metrics' + '\n')

sampling_depth = 20000

os.system('bash/q2pipeline/q2_core_metrics.sh' + str(sampling_depth))

print('\n' + 'Beta Group Significance' + '\n')

df_meta = pd.read_csv('dataflow/00-meta/sample-metadata.tsv', sep = '\t')
columns = list(df_meta)
columns.remove('#SampleID')

for cname in columns:
	output_f = 'dataflow/02-qiime-viz/weighted-unifrac-' + str(cname) + '-beta-significance.qzv'
	command = 'bash/q2pipeline/q2_beta_sig.sh' + ' ' + str(cname) + ' ' + output_f
	os.system(command)

data_params.update({'Sampling Depth, Core Metrics': sampling_depth})
data_params.update({'Paired': paired})

df_data_params = pd.DataFrame.from_dict(data_params, orient="index")
df_data_params.to_csv("dataflow/00-logs/selected_parameters.csv")
