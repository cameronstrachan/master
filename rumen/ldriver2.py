# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

#os.system("source activate qiime2-2018.11")

### RUN QIIME ON HENDERSON DATA
runqiime = input("\n" + "Run Qiime on data from Henderson et al. 2015? (y or n):")

if runqiime == 'y':
	sg.runqiime(inputfolderloc='dataflow/01-fastq/henderson2015', paired=False, numcores=40)


### THEN ANALYSIS WITH DESeq_henderson2015_97 Rmardown

extractseqs = input("\n" + "Extract seqs with differential abundance between sample defined on the presence of Lactobacillus? (y or n):")

if extractseqs == 'y':

### select seq ids from metadata
	meta_df = pd.read_csv('dataflow/00-meta/lacto_signal_differential.csv', low_memory=False)

	seqs_decrease = meta_df[meta_df['direction'] == 'decrease']
	seqs_decrease = seqs_decrease['asv_id'].tolist()


	seqs_increase = meta_df[meta_df['direction'] == 'increase']
	seqs_increase = seqs_increase['asv_id'].tolist()



	file_obj = sc.Fasta('henderson2015-4_194-99.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputLocation('dataflow/01-nucl/')

	file_obj.setOutputName('lacto_prevo_decrease.fasta')
	file_obj.subsetfasta(seqlist = seqs_decrease , headertag='decrease')

	file_obj.setOutputName('lacto_prevo_increase.fasta')
	file_obj.subsetfasta(seqlist = seqs_increase, headertag='increase')


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

runscript = input("\n" + "Extract the representative seqs from the blast table? (y or n):")

if runscript == 'y':
	os.system("python src/python/representative2relatedseqs.py")

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

runscript = input("\n" + "Extract the genomes seqs from the blast table? (y or n):")

if runscript == 'y':
	os.system("python src/python/blasttables2seqs.py")

runblast = input("\n" + "Concatenate sequences from genomes and? (y or n):")

if runblast == 'y':
	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes.fasta', filenames=["lacto_signal_differential_all_seqs_genomes.fasta", "lacto_signal_differential_all_seqs.fasta"])

#os.system("source deactivate qiime2-2018.11")
