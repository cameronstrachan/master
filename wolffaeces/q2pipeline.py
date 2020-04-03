import os, sys
import pandas as pd

# colours
CRED = '\033[91m'
CGREEN  = '\33[32m'
CEND = '\033[0m'

# STEP 1. Make directories

if os.path.exists('dataflow') == False:
	os.mkdir('dataflow')

check = input("\n" + 'Single end amplicon pipeline' + '\n' + '\n' + 'Hit any key to continue')

dirs = ['01-fastq', '00-meta', '02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

# STEP 2. IMPORT DATA.

print('\n' + CRED + 'DATA IMPORT' + CEND + '\n')

os.system('q2pipeline/q2_import.sh \'SampleData[SequencesWithQuality]\'')

print('\n' + CGREEN + 'Visualize dataflow/02-qiime-viz/demux-trimmed.qzv at https://view.qiime2.org/' + CEND + '\n')

# RUN DADA2

print('\n' + CRED + 'DADA2' + CEND + '\n')

cores = str(input('\n' + 'Number of cores to use with DADA2 (interger):'))

cut_off1 = str(input("\n" + "Left Cutoff? (interger):"))

cut_off2 = str(input("\n" + "Length Cutoff? (interger):"))


command = 'q2pipeline/q2_dada2-single.sh ' + cut_off1 + ' ' + cut_off2  + ' ' + cores
print('\n')
os.system(command)

data_params = {'Left Cutoff':cut_off1, "Length Cutoff":cut_off2}

# STEP 3. Save parameters to the log directory

df_data_params = pd.DataFrame.from_dict(data_params, orient="index")
df_data_params.to_csv("dataflow/00-logs/selected_cutoffs.csv")

# STEP 4. Export seqs and table

os.system('q2pipeline/q2_export.sh')
