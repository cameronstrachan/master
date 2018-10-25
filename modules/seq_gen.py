#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Bio import SearchIO
import os,sys
import pandas as pd
import numpy as np

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc

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