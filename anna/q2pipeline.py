import os, sys
import pandas as pd

# colours
CRED = '\033[91m'
CGREEN  = '\33[32m'
CEND = '\033[0m'



# STEP 1. Make directories and print start message.

print("\n" + CRED + 'This is a qimme2 wrapper to standardize running qimme2' + CEND)

if os.path.exists('dataflow') == False:
	os.mkdir('dataflow')

if os.path.exists('dataflow/01-fastq') == False:
	os.mkdir('dataflow/01-fastq')

if os.path.exists('dataflow/01-fastq/trimmed') == False:
	os.mkdir('dataflow/01-fastq/trimmed')

start_message = 'This pipeline is for single end (ex. 454) 16s sequencing data. The zipped and demultiplexed sequencing data must be in dataflow/01-fastq/ with the illumina naming (ex. SampleName_SampleNumber_L001_R1_001.fastq.gz). Primers will not be used, as we are combining many different 454 datasets.'

# in fastq folder, run the following renaming
# find . -name '*.fastq.gz' -exec bash -c ' mv $0 ${0/\_pass/_1_L001_R1_001}' {} \;

check = input("\n" + start_message + '\n' + '\n' + 'Hit any key to continue')

dirs = ['02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']
#dirs_control = [d + '-control' for d in dirs]

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

# this data is getting moved to a trimmed folder, but because the datasets are
# from different sources, the data is not being trimmed until dada2 where we will
# remove enough base bairs to make sure the primers are gone.

command = 'cp dataflow/01-fastq/* dataflow/01-fastq/trimmed'
os.system(command)

# STEP 2. Run DADA2.

print('\n' + CRED + 'DATA IMPORT' + CEND + '\n')


os.system('../bash/q2pipeline/q2_import.sh \'SampleData[SequencesWithQuality]\'')

print('\n' + CGREEN + 'Visualize dataflow/02-qiime-viz/demux-trimmed.qzv at https://view.qiime2.org/' + CEND + '\n')

print('\n' + CRED + 'DADA2' + CEND + '\n')

cores = str(input('\n' + 'Number of cores to use with DADA2 (interger):'))

left = str(input("\n" + "Left Cutoff? (interger):"))

trunc = str(input("\n" + "Length Cutoff? (interger):"))

command = '../bash/q2pipeline/q2_dada2-single.sh ' + left + ' ' + trunc + ' ' + cores
print('\n')
os.system(command)

data_params = {'Left Cutoff':left,'Length Cutoff':trunc}

# STEP 3. Cluster sequences at 99% identity.

print('\n' + CRED + '99% CLUSTERING' + CEND + '\n')

os.system('../bash/q2pipeline/q2_clustering99.sh')
