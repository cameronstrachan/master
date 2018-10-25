#!/Users/cameronstrachan/anaconda/bin/ python3
# -*- coding: utf-8 -*-

### WRITING A SCRIPT TO ANALYZE INDIVIDUAL FOSMIDS

# python libraries
import os, sys
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg

### PROCESS SINGLE FOSMIDS

### SELECT SINGLE FOSMIDS FROM META DATA
meta_df = pd.read_csv('dataflow/00-meta/static_files.csv', low_memory=False)
meta_df_subset_single_fosmids = meta_df[meta_df['description'] == 'single fosmid']
single_fosmids = meta_df_subset_single_fosmids['file_name'].tolist()

### LENGTH CUTOFF and RUN PRODIGAL
for file in single_fosmids:
	# contruct object
	file_obj = sc.Fasta(file, 'dataflow/01-nucl/')

	# set output name, location
	file_obj.setOutputName(file)
	file_obj.setOutputLocation('dataflow/01-nucl-lengthcutoff/')

	# run length cut off
	file_obj.lengthcutoff(length = 1500)

	# set input and output location 
	file_obj.setLocation('dataflow/01-nucl-lengthcutoff/')
	file_obj.setOutputLocation('dataflow/01-prot/')
	
	# run prodigal 
	file_obj.runprodigal()

### RUN ONLINE BLAST OF SINGLE FOSMIDS
runblast = input("\n" + "Run online blast of single fosmids? (y or n):")

if runblast == 'y':
	for file in single_fosmids:
		file_obj = sc.Fasta(file, 'dataflow/01-prot/')
		file_obj.setOutputLocation('dataflow/02-blast/')
		file_obj.runonlineblast()

# combine XML outputs into single table

combinexml = input("\n" + "Combine XMLs from single fosmid blast into a table? (y or n):")

if combinexml == 'y':
	
	prot_files = [f for f in os.listdir('dataflow/01-prot/') if f.endswith(".fasta")]
	blast_files = [f for f in os.listdir('dataflow/02-blast/') if f.endswith(".xml")]

	sg.blastxmltotable(xmlinputfolder='dataflow/02-blast/', blastinputfolder='dataflow/01-prot/',outputpath='dataflow/03-blast-tables/single_fosmids_refseq_prot.csv', xmlfilenames=blast_files, blastfilename=prot_files)


### FOSDB NUCL DATABASE
file_obj = sc.Fasta('fosDB.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('fosDB_5000.fasta')
file_obj.setOutputLocation('dataflow/01-nucl-lengthcutoff/')
file_obj.lengthcutoff(length = 5000)

runmakedb = input("\n" + "Make nucl blast database with fosDB? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('fosDB_5000.fasta', 'dataflow/01-nucl-lengthcutoff/')
	file_obj.setOutputName('fosDB_5000_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()

### PROCESS END SEQS

### SELECT END SEQS FROM META DATA
meta_df_subset_end_seqs = meta_df[meta_df['description'] == 'fosmid end sequences']
end_seqs = meta_df_subset_end_seqs['file_name'].tolist()
outfilepath = 'dataflow/01-nucl/end_seqs.fasta'

### CONCATENATE END SEQS
sg.concat(inputfolder='dataflow/01-nucl/', outputpath=outfilepath, filenames=end_seqs)

### RUN ENDSEQ BLAST
runblast = input("\n" + "Run end seq blast on trimmed fosDB? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('end_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('end_seqs_fosDB_nucl')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(db='fosDB_5000_db')


# COMPARE SINGLE FOSMIDS TO PCC1 and TRANSPOSON
runmakedb = input("\n" + "Make nucl blast database with pcc1 and transposon? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('pcc1_transposon.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('pcc1_transposon_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()


sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/single_fosmids.fasta', filenames=single_fosmids)

runblast = input("\n" + "Run single fosmids blast against pcc1 and transposon? (y or n):")

if runblast == 'y':
	for file in single_fosmids:
		file_obj = sc.Fasta(file, 'dataflow/01-nucl-lengthcutoff/')
		filename_noext = file.split('.f')[0]
		file_obj.setOutputName(filename_noext + '_pcc1_transposon_nucl')
		file_obj.setOutputLocation('dataflow/03-blast-tables/')
		file_obj.runblast(db='pcc1_transposon_db', max_target_seqs=10)




