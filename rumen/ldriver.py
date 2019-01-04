# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN QIIME ON HENDERSON DATA
runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=40)


### THEN ANALYSIS WITH DESeq_henderson2015_97 Rmardown

extractseqs = input("\n" + "Extract seqs with differential abundance between sample defined on the presence of Lactobacillus? (y or n):")

if extractseqs == 'y':

### select seq ids from metadata
	meta_df = pd.read_csv('dataflow/00-meta/lacto_signal_differential.csv', low_memory=False)

	seqs_neg_cor = meta_df[meta_df['direction'] == 'neg_cor']
	seqs_neg_cor = seqs_neg_cor['asv_id'].tolist()


	seqs_pos_cor = meta_df[meta_df['direction'] == 'pos_cor']
	seqs_pos_cor = seqs_pos_cor['asv_id'].tolist()



	file_obj = sc.Fasta('henderson2015-4_194-97.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputLocation('dataflow/01-nucl/')

	file_obj.setOutputName('lacto_prevo_decrease.fasta')
	file_obj.subsetfasta(seqlist = seqs_neg_cor , headertag='decrease')

	file_obj.setOutputName('lacto_prevo_increase.fasta')
	file_obj.subsetfasta(seqlist = seqs_pos_cor, headertag='increase')


	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_signal_differential_seqs.fasta', filenames=["lacto_prevo_decrease.fasta", "lacto_prevo_increase.fasta"])


### THIS GOES FROM THE (97% seqs to the 100% seqs)

runmakedb = input("\n" + "Make nucl blast database with asv seqs from Henderson 2015 data (trimmed at 4 and 194)? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('henderson2015-4_194-100.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputName('henderson2015-4_194-100_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()

runblast = input("\n" + "Blast Henderson 97 clustered asvs against 100 clustered asvs (trimmed at 4 and 194)? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='henderson2015-4_194-100_db')

### HERE FROM RUN R SCRIPT TO EXTRACT THE SEQs from the above blast table

runblast = input("\n" + "Blast the 100 percent seqs against rumen genomes? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_all_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_rumen_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='rumen_genomes_db')


runblast = input("\n" + "Blast the 100 percent seqs against prevotella genomes? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_all_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_prevotella_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=10, db='prevotella_genomes_db')

### THEN I RUN R SCRIPT TO EXTRACT THE SEQUENCES FROM THE GENOME HITS
