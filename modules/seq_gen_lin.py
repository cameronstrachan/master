#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from Bio import SearchIO
import os,sys
import pandas as pd
import numpy as np
import subprocess
from shutil import copyfile

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc

def concat(inputfolder='path/to/input/', outputpath='path/to/output/file.txt', filenames=[]):
	
	if not os.path.exists(outputpath):
		with open(outputpath, 'w') as outfile:
		    for file in filenames:
		        with open(inputfolder + file) as infile:
		            for line in infile:
		                outfile.write(line)
	else:
		print("\n" + 'File already exists: ' + outputpath)



def blastxmltotable(xmlinputfolder='path/to/input/', blastinputfolder= 'path/to/input/',outputpath='path/to/output/file.txt', xmlfilenames=[], blastfilename=[]):
	
	headerdictdict = {}

	for file in blastfilename:
		file_obj = sc.Fasta(file, blastinputfolder)
		headerdict = file_obj.fasta2headermap()
		headerdictdict.update(headerdict)

	df = pd.DataFrame(headerdictdict, index=[0]).transpose()
	df.columns = ['header']

	df['qseq_length'] = np.nan
	df['sseq_length'] = np.nan
	df['sseq_accession'] = np.nan
	df['sseq_description'] = np.nan
	df['bitscore'] = np.nan
	df['evalue'] = np.nan
	df['matched_residues'] = np.nan
	df['alignment_length'] = np.nan
	df['percent_identity'] = np.nan

	for file in xmlfilenames:
	    qresult = SearchIO.read(xmlinputfolder + file, 'blast-xml')
	    row_index = file.split('.xml')[0]
	    df.loc[df.index == row_index, 'qseq_length'] = qresult.seq_len
	    if len(qresult) != 0:
	        df.loc[df.index == row_index, 'sseq_length'] = qresult[0].seq_len
	        df.loc[df.index == row_index, 'sseq_accession'] = qresult[0].accession
	        df.loc[df.index == row_index, 'sseq_description'] = qresult[0].description
	        df.loc[df.index == row_index, 'bitscore'] = qresult[0][0].bitscore
	        df.loc[df.index == row_index, 'evalue'] = qresult[0][0].evalue
	        df.loc[df.index == row_index, 'matched_residues'] = qresult[0][0].ident_num
	        df.loc[df.index == row_index, 'alignment_length'] = qresult[0][0].aln_span
	        per_id = (qresult[0][0].ident_num / qresult[0].seq_len)*100
	        df.loc[df.index == row_index, 'percent_identity'] = per_id
	    else:
	        pass
	    
	df = df.dropna()
	df.to_csv(outputpath)

def runqiime(inputfolderloc='path/to/input', paired=True, numcores=7):

	# data must be in form ERX1660185_1_L001_R1_001.fastq.gz

	inputfolder = inputfolderloc
	foldername = inputfolder.split('/')[2]

	if paired == True:
		subprocess.call(['/home/strachan/master/bash/qiime_import_paired_lin.sh', inputfolder])
		#pass
	else: 
		subprocess.call(['/home/strachan/master/bash/qiime_import_single_lin.sh', inputfolder])
		#pass

	print("\n" + "Visualize dataflow/02-qiime/demux-single-end.qzv using online too at:" + "\n")
	print("https://view.qiime2.org/" + "\n")

	if paired == True:
		
		lengthcutoff = input("\n" + "Forward Read, Left Cutoff? (interger):")

		lengthcutoff1 = int(lengthcutoff)

		lengthcutoff = input("\n" + "Reverse Read, Left Cutoff? (interger):")

		lengthcutoff2 = int(lengthcutoff)

		lengthcutoff = input("\n" + "Forward Read, Length Cutoff? (interger):")

		lengthcutoff3 = int(lengthcutoff)

		lengthcutoff = input("\n" + "Reverse Read, Length Cutoff? (interger):")

		lengthcutoff4 = int(lengthcutoff)

		outputprefixseqs = 'dataflow/03-asv-seqs/' + foldername + '-' + str(lengthcutoff1) + '_' + str(lengthcutoff3) + '_' + str(lengthcutoff2) + '_' + str(lengthcutoff4)
		outputprefixstabs = 'dataflow/03-asv-table/' + foldername + '-' + str(lengthcutoff1) + '_' + str(lengthcutoff3) + '_' + str(lengthcutoff2) + '_' + str(lengthcutoff4)
		outputprefixstaxa = 'dataflow/03-asv-taxonomy/' + foldername + '-' + str(lengthcutoff1) + '_' + str(lengthcutoff3) + '_' + str(lengthcutoff2) + '_' + str(lengthcutoff4)

	else:

		lengthcutoff = input("\n" + "Left Cutoff? (interger):")

		lengthcutoff1 = int(lengthcutoff)

		lengthcutoff = input("\n" + "Length Cutoff? (interger):")

		lengthcutoff2 = int(lengthcutoff)

		outputprefixseqs = 'dataflow/03-asv-seqs/' + foldername + '-' + str(lengthcutoff1) + '_' + str(lengthcutoff2)
		outputprefixstabs = 'dataflow/03-asv-table/' + foldername + '-' + str(lengthcutoff1) + '_' + str(lengthcutoff2)
		outputprefixstaxa = 'dataflow/03-asv-taxonomy/' + foldername + '-' + str(lengthcutoff1) + '_' + str(lengthcutoff2)


	if paired == True:
		subprocess.call(['/home/strachan/master/bash/run_qiime_paired_lin.sh', str(lengthcutoff1), str(lengthcutoff2), str(lengthcutoff3), str(lengthcutoff4), str(numcores)])
		#pass
	else:
		subprocess.call(['/home/strachan/master/bash/run_qiime_single_lin.sh', str(lengthcutoff1), str(lengthcutoff2), str(numcores)])
		#pass

	subprocess.call('/home/strachan/master/bash/qiime_export_lin.sh')

	table_merge = 'dataflow/02-qiime-merge/' + 'table' + '_' + foldername + '.qza' 
	copyfile('dataflow/02-qiime/table.qza', table_merge)

	seq_merge = 'dataflow/02-qiime-merge/' + 'rep-seqs' + '_' +foldername + '.qza' 
	copyfile('dataflow/02-qiime/rep-seqs.qza', seq_merge)	

	#os.rename('dataflow/03-asv-table/taxonomy.tsv', outputprefixstaxa + '-fc-gg-full.txt')

	os.rename('dataflow/03-asv-seqs/dna-sequences-100.fasta', outputprefixseqs + '-100.fasta')
	os.rename('dataflow/03-asv-seqs/dna-sequences-99.fasta', outputprefixseqs + '-99.fasta')
	os.rename('dataflow/03-asv-seqs/dna-sequences-97.fasta', outputprefixseqs + '-98.fasta')
	os.rename('dataflow/03-asv-seqs/dna-sequences-97.fasta', outputprefixseqs + '-97.fasta')
	os.rename('dataflow/03-asv-table/feature-table-100.txt', outputprefixstabs + '-100.txt')
	os.rename('dataflow/03-asv-table/feature-table-99.txt', outputprefixstabs + '-99.txt')
	os.rename('dataflow/03-asv-table/feature-table-97.txt', outputprefixstabs + '-98.txt')
	os.rename('dataflow/03-asv-table/feature-table-97.txt', outputprefixstabs + '-97.txt')



def runqiimemerge(file1folder='wetzels2018', file2folder='wu2018'):

	table1 = 'table_' + file1folder + '.qza'
	table2 = 'table_' + file2folder + '.qza'

	seqs1 = 'rep-seqs_' + file1folder + '.qza'
	seqs2 = 'rep-seqs_' + file2folder + '.qza'

	subprocess.call(['/home/strachan/master/bash/merge_qiime_lin.sh', str(table1), str(table2), str(seqs1), str(seqs2)])
	subprocess.call('/home/strachan/master/bash/qiime_export_merge_lin.sh')

	outputprefixseqs = 'dataflow/03-asv-seqs-merge/' + file1folder + '_' + file2folder
	outputprefixstabs = 'dataflow/03-asv-table-merge/' + file1folder + '_' + file2folder

	os.rename('dataflow/03-asv-seqs-merge/dna-sequences-100.fasta', outputprefixseqs + '-100.fasta')
	os.rename('dataflow/03-asv-seqs-merge/dna-sequences-99.fasta', outputprefixseqs + '-99.fasta')
	os.rename('dataflow/03-asv-seqs-merge/dna-sequences-97.fasta', outputprefixseqs + '-97.fasta')
	os.rename('dataflow/03-asv-table-merge/feature-table-100.txt', outputprefixstabs + '-100.txt')
	os.rename('dataflow/03-asv-table-merge/feature-table-99.txt', outputprefixstabs + '-99.txt')
	os.rename('dataflow/03-asv-table-merge/feature-table-97.txt', outputprefixstabs + '-97.txt')