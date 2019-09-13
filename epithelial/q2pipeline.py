import os, sys
import pandas as pd

# colours
CRED = '\033[91m'
CGREEN  = '\33[32m'
CEND = '\033[0m'

# STEP 1. Specify paied or unpaired. Make directories.

print("\n" + CRED + 'This is a qimme2 wrapper to standardize running qimme2 without primer trimming. The first argument needs to state paired or single and the second needs to specify the subfolder with the data in 01-fastq.' + CEND)

if str(sys.argv[1]) == 'single':
	print('\n' + 'Processing single end data')
	paired = False
elif str(sys.argv[1]) == 'paired':
	print('\n' + 'Processing paired end data')
	paired = True

subfolder = sys.argv[2]

if os.path.exists('dataflow') == False:
	os.mkdir('dataflow')

dirs = ['00-meta', '01-fastq', '02-qiime', '02-qiime-viz', '03-asv-seqs', '03-asv-table', '00-logs']

for dir in dirs:
	dir_to_make = 'dataflow/' + dir

	if os.path.exists(dir_to_make) == False:
		os.mkdir(dir_to_make)

# STEP 2. Run DADA2.

print('\n' + CRED + 'DATA IMPORT' + CEND + '\n')

if paired == True:
	os.system('../bash/q2pipeline/q2_import.sh \'SampleData[PairedEndSequencesWithQuality]\'' + ' ' + subfolder)
else:
	os.system('../bash/q2pipeline/q2_import.sh \'SampleData[SequencesWithQuality]\'' + ' ' + subfolder)

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
	os.system(command)

	data_params = {'Forward Read, Left Cutoff':left_forward,'Reverse Read, Left Cutoff':left_reverse, "Forward Read, Length Cutoff":trunc_forward, "Reverse Read, Length Cutoff":trunc_reverse}

else:

	left = str(input("\n" + "Left Cutoff? (interger):"))

	trunc = str(input("\n" + "Length Cutoff? (interger):"))

	command = '../bash/q2pipeline/q2_dada2-single.sh ' + left + ' ' + trunc + ' ' + cores
	print('\n')
	os.system(command)

	data_params = {'Left Cutoff':left,'Length Cutoff':trunc}

data_params_csv_path = 'dataflow/00-meta/' + subfolder + '_' + 'length_cutoffs.csv'

with open(data_params_csv_path, 'w') as f:
	for key in data_params.keys():
		f.write("%s,%s\n"%(key,data_params[key]))

qiime_table_rename = 'dataflow/02-qiime/table' + '_' + subfolder + '.qza'

os.rename('dataflow/02-qiime/table.qza', qiime_table_rename)

qiime_seqs_rename = 'dataflow/02-qiime/rep-seqs' + '_' + subfolder + '.qza'

os.rename('dataflow/02-qiime/rep-seqs.qza', qiime_seqs_rename)

qiime_stats_rename = 'dataflow/02-qiime/stats-dada2' + '_' + subfolder + '.qza'

os.rename('dataflow/02-qiime/stats-dada2.qza', qiime_stats_rename)

# STEP 3. Cluster sequences at 99% identity.

print('\n' + CRED + '99% CLUSTERING' + CEND + '\n')

os.system('../bash/q2pipeline/q2_clustering99.sh')

qiime_table_rename = 'dataflow/02-qiime/table-dn-99' + '_' + subfolder + '.qza'

os.rename('dataflow/02-qiime/table-dn-99.qza', qiime_table_rename)

qiime_seqs_rename = 'dataflow/02-qiime/rep-seqs-dn-99' + '_' + subfolder + '.qza'

os.rename('dataflow/02-qiime/rep-seqs-dn-99.qza', qiime_seqs_rename)

# STEP 4. Rename files.

fasta_rename = 'dataflow/03-asv-seqs/' + subfolder + '_99.fasta'

os.rename('dataflow/03-asv-seqs/dna-sequences-99.fasta', fasta_rename)

table_rename = 'dataflow/03-asv-table/' + subfolder + '_99.txt'

os.rename('dataflow/03-asv-table/feature-table-99.txt', table_rename)
