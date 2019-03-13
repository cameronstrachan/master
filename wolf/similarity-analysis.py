import os, sys
import pandas as pd

metadata = 'sample-metadata.tsv'

#files = ['feature-table-no-contam-all-feces.txt', 'feature-table-no-contam-all-skin.txt', 'feature-table-no-contam-wild_animals-feces.txt', 'feature-table-no-contam-wild_animals-skin.txt', 'feature-table-no-contam-pet_animals-feces.txt', 'feature-table-no-contam-pet_animals-skin.txt', 'feature-table-no-contam-wild_animals-skin_pack3.txt', 'feature-table-no-contam-wild_animals-feces_pack3.txt', 'feature-table-no-contam-all_animals-skin.txt', 'feature-table-no-contam-all_animals-feces.txt']

files = ['feature-table-no-contam-all_animals-skin.txt', 'feature-table-no-contam-all_animals-feces.txt']

df_meta = pd.read_csv('dataflow/00-meta-merge/sample-metadata.tsv', sep = '\t')
columns = list(df_meta)
columns.remove('#SampleID')

for file in files:
	outname = file.split('-')[4] + '-' + file.split('-')[5].split('.')[0]
	command = './q2-commands-similarity.sh' + ' ' + metadata + ' ' + outname + ' ' + file
	os.system(command)
	
	for cname in columns:
		output_f = 'dataflow/02-qiime-viz-temp/beta-sig/weighted-unifrac-' + str(cname) + '-' + outname + '-beta-significance.qzv'
		command = '../bash/q2pipeline_temp/q2_beta_sig-weighted.sh' + ' ' + str(cname) + ' ' + output_f 
		os.system(command)

	for cname in columns:
		output_f = 'dataflow/02-qiime-viz-temp/beta-sig/unweighted-unifrac-' + str(cname) + '-' + outname + '-beta-significance.qzv'
		command = '../bash/q2pipeline_temp/q2_beta_sig-unweighted.sh' + ' ' + str(cname) + ' ' + output_f
		os.system(command)

	for cname in columns:
		output_f = 'dataflow/02-qiime-viz-temp/beta-sig/bray-curtis-' + str(cname) + '-' + outname + '-beta-significance.qzv'
		command = '../bash/q2pipeline_temp/q2_beta_sig-bray.sh' + ' ' + str(cname) + ' ' + output_f
		os.system(command)
		
# even single packs are compared, i need to fix this in the meta data 
