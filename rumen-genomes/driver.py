# python libraries
import os,sys

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/Desktop/master/') 
from modules import seq_scrape as ss
from modules import seq_core as sc


gb_dir = 'dataflow/01-gb/'
ss.ncbigenomescrape('bacteroides ovatus', location=gb_dir)
gb_prot_out = 'dataflow/01-prot/'
gb_nucl_out = 'dataflow/01-nucl/'
extention_add = '_genbank.fasta'

files = [f for f in os.listdir(gb_dir) if f.endswith(".gb")]

for file in files:
	file_obj = sc.GenBank(file, gb_dir)
	# output location
	file_obj.setOutputLocation(gb_prot_out)

	# output name
	file_out = file.split('.g')[0] + extention_add
	file_obj.setOutputName(file_out)

	# run genbank to prot
	file_obj.genbank2protfasta()

	# output location
	file_obj.setOutputLocation(gb_nucl_out)

	# run genbank to prot
	file_obj.genbank2nuclfasta()