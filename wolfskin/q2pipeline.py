import os, sys
import pandas as pd

# colours
CRED = '\033[91m'
CGREEN  = '\33[32m'
CEND = '\033[0m'

# STEP 1. Make directories

if os.path.exists('dataflow') == False:
	os.mkdir('dataflow')

check = input("\n" + 'Paired end amplicon pipeline' + '\n' + '\n' + 'Hit any key to continue')

dirs = ['01-fastq', '00-meta', '02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

# STEP 2. IMPORT DATA.

print('\n' + CRED + 'DATA IMPORT' + CEND + '\n')

os.system('q2pipeline/q2_import.sh \'SampleData[PairedEndSequencesWithQuality]\'')

print('\n' + CGREEN + 'Visualize dataflow/02-qiime-viz/demux-trimmed.qzv at https://view.qiime2.org/' + CEND + '\n')

# RUN DADA2

print('\n' + CRED + 'DADA2' + CEND + '\n')

cores = str(input('\n' + 'Number of cores to use with DADA2 (interger):'))

left_forward = str(input("\n" + "Forward Read, Left Cutoff? (interger):"))

left_reverse = str(input("\n" + "Reverse Read, Left Cutoff? (interger):"))

trunc_forward = str(input("\n" + "Forward Read, Length Cutoff? (interger):"))

trunc_reverse = str(input("\n" + "Reverse Read, Length Cutoff? (interger):"))

command = '../bash/q2pipeline/q2_dada2-paired.sh ' + left_forward + ' ' + left_reverse + ' ' + trunc_forward + ' ' + trunc_reverse + ' ' + cores
print('\n')
os.system(command)

data_params = {'Forward Read, Left Cutoff':left_forward,'Reverse Read, Left Cutoff':left_reverse, "Forward Read, Length Cutoff":trunc_forward, "Reverse Read, Length Cutoff":trunc_reverse}

# STEP 3. Save parameters to the log directory

df_data_params = pd.DataFrame.from_dict(data_params, orient="index")
df_data_params.to_csv("dataflow/00-logs/selected_cutoffs.csv")
