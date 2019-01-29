import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN DIFFERENTIAL ABUNDANCE HENDERSON 2015
### Environment: source activate anaconda

runcommand = input("\n" + "Run sample classification (Lactobacillus)? (y or n):")

if runcommand == 'y':
	os.system("Rscript src/R/generate_df_metrics_lacto_detectable.R")


runcommand = input("\n" + "Run DEseq? (y or n):")

if runcommand == 'y':
	os.system("Rscript src/R/generate_DESeq_sigtab_detectable.R")

runcommand = input("\n" + "Select seqs from DEseq results? (y or n):")

if runcommand == 'y':
	os.system("Rscript src/R/generate_lacto_differential_select.R ")

extractseqs = input("\n" + "Extract seqs with differential abundance between sample defined on the presence of Lactobacillus? (y or n):")

if extractseqs == 'y':

### delete the output files

runcommand = input("\n" + "Delete the output files from the pipeline?")

if runcommand == 'y':

	outputfiles = ["dataflow/01-nucl/lacto_prevo_decrease.fasta", "dataflow/01-nucl/lacto_prevo_increase.fasta", "dataflow/01-nucl/lacto_signal_differential_seqs.fasta", "dataflow/03-blast-tables/lacto_signal_differential_seqs_mapped", "dataflow/03-blast-tables/lacto_signal_differential_all_seqs_tags_rumen_genomes_mapped", "dataflow/03-blast-tables/lacto_signal_differential_all_seqs_tags_prevotella_genomes_mapped", "dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes.fasta", "dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes_short.fasta"]

	for ofile in outputfiles:

		if os.path.exists(ofile):
		  os.remove(ofile)
		else:
		  print("The file " + ofile + " does not exist")

### select seq ids from metadata
	meta_df = pd.read_csv('dataflow/00-meta/lacto_signal_differential.csv', low_memory=False)

	seqs_decrease = meta_df[meta_df['direction'] == 'decrease']
	seqs_decrease = seqs_decrease['asv_id'].tolist()


	seqs_increase = meta_df[meta_df['direction'] == 'increase']
	seqs_increase = seqs_increase['asv_id'].tolist()



	file_obj = sc.Fasta('henderson2015-20_320-99.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputLocation('dataflow/01-nucl/')

	file_obj.setOutputName('lacto_prevo_decrease.fasta')
	file_obj.subsetfasta(seqlist = seqs_decrease , headertag='decrease')

	file_obj.setOutputName('lacto_prevo_increase.fasta')
	file_obj.subsetfasta(seqlist = seqs_increase, headertag='increase')


	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_signal_differential_seqs.fasta', filenames=["lacto_prevo_decrease.fasta", "lacto_prevo_increase.fasta"])


### THIS GOES FROM THE (97% seqs to the 100% seqs)

runmakedb = input("\n" + "Make nucl blast database with asv seqs from Henderson 2015 data (trimmed at 20 and 320)? (y or n):")

if runmakedb == 'y':
	file_obj = sc.Fasta('henderson2015-20_320-100.fasta', 'dataflow/03-asv-seqs/')
	file_obj.setOutputName('henderson2015-20_320-100_db')
	file_obj.setOutputLocation('dataflow/02-blast-db/')
	file_obj.runmakeblastdb()

runblast = input("\n" + "Blast Henderson 99 clustered asvs against 100 clustered asvs (trimmed at 20 and 320)? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_seqs.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_seqs_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='henderson2015-20_320-100_db')

runscript = input("\n" + "Extract the representative seqs from the blast table? (y or n):")

if runscript == 'y':
	os.system("python src/python/representative2relatedseqs.py")

runblast = input("\n" + "Blast the 100 percent seqs against rumen genomes? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_all_seqs_tags.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_tags_rumen_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=100, db='rumen_genomes_db')


runblast = input("\n" + "Blast the 100 percent seqs against prevotella genomes? (y or n):")

if runblast == 'y':
	file_obj = sc.Fasta('lacto_signal_differential_all_seqs_tags.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_tags_prevotella_genomes_mapped')
	file_obj.setOutputLocation('dataflow/03-blast-tables/')
	file_obj.runblast(max_target_seqs=10, db='prevotella_genomes_db')

runscript = input("\n" + "Extract the genomes seqs from the blast table (currently only taking from rumen genomes)? (y or n):")

if runscript == 'y':
	os.system("python src/python/blasttables2seqs.py")

runblast = input("\n" + "Concatenate sequences from rumen genomes and tags? (y or n):")

if runblast == 'y':
	sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes.fasta', filenames=["lacto_signal_differential_all_seqs_genomes.fasta", "lacto_signal_differential_all_seqs_tags.fasta"])

	file_obj = sc.Fasta('lacto_signal_differential_all_seqs_tags_genomes.fasta', 'dataflow/01-nucl/')
	file_obj.setOutputName('lacto_signal_differential_all_seqs_tags_genomes_short.fasta')
	file_obj.setOutputLocation('dataflow/01-nucl/')


	headers = file_obj.fasta2headermap()
	l = []

	for key, value in headers.items():
		l.append(key)

	file_obj.subsetfasta(seqlist = l , headertag='number', replace=':', length=30)


runcommand = input("\n" + "Run muscle on rumen genome extracted seqs and tags? (y or n):")

if runcommand == 'y':
	os.system("../bin/muscle -in dataflow/01-nucl/lacto_signal_differential_all_seqs_tags_genomes_short.fasta -out dataflow/03-alignments/lacto_signal_differential_all_seqs_tags_genomes_alignment.afa")

runcommand = input("\n" + "Run Gblocks on rumen genome extracted seqs and tags? (y or n):")

if runcommand == 'y':
	os.system("../bin/Gblocks dataflow/03-alignments/lacto_signal_differential_all_seqs_tags_genomes_alignment.afa -t=d -b6=n")

runcommand = input("\n" + "Run FastTree on rumen genome extracted seqs and tags? (y or n):")

if runcommand == 'y':
	os.system("../bin/FastTree -gtr -nt dataflow/03-alignments/lacto_signal_differential_all_seqs_tags_genomes_alignment.afa-gb > dataflow/03-trees/lacto_signal_differential_all_seqs_tags_genomes_tree.newick")

