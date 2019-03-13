metadata=$1
outname=$2
inname=$3

biom convert -i dataflow/03-asv-table-merge/$inname -o dataflow/03-asv-table-merge/feature-table-temp.biom --table-type="OTU table" --to-hdf5
  
qiime tools import \
	--input-path dataflow/03-asv-table-merge/feature-table-temp.biom \
	--type "FeatureTable[Frequency]" \
	--output-path dataflow/02-qiime-temp/table-dn-97-temp.qza

qiime feature-table filter-seqs \
	--i-data dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
	--i-table dataflow/02-qiime-temp/table-dn-97-temp.qza \
	--o-filtered-data dataflow/02-qiime-temp/rep-seqs-dn-97-temp.qza

qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences dataflow/02-qiime-temp/rep-seqs-dn-97-temp.qza \
  --o-alignment dataflow/02-qiime-temp/aligned-rep-seqs-dn-97-temp.qza \
  --o-masked-alignment dataflow/02-qiime-temp/masked-aligned-rep-seqs-dn-97-temp.qza \
  --o-tree dataflow/02-qiime-temp/unrooted-tree-temp.qza \
  --o-rooted-tree dataflow/02-qiime-temp/rooted-tree-temp.qza

qiime diversity alpha-rarefaction \
  --i-table dataflow/02-qiime-temp/table-dn-97-temp.qza \
  --i-phylogeny dataflow/02-qiime-temp/rooted-tree-temp.qza \
  --p-max-depth 14000 \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-alpha-rarefaction.qzv

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny dataflow/02-qiime-temp/rooted-tree-temp.qza \
  --i-table dataflow/02-qiime-temp/table-dn-97-temp.qza \
  --p-sampling-depth 14000 \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --output-dir dataflow/02-qiime-core-metrics

mv dataflow/02-qiime-core-metrics/*.qza dataflow/02-qiime-temp/
mv dataflow/02-qiime-core-metrics/*.qzv dataflow/02-qiime-viz-temp/
rm -r dataflow/02-qiime-core-metrics/


qiime diversity alpha \
  --i-table dataflow/02-qiime-temp/rarefied_table.qza \
  --p-metric observed_otus \
  --o-alpha-diversity dataflow/02-qiime-temp/observed_otus_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-temp/rarefied_table.qza \
  --p-metric ace \
  --o-alpha-diversity dataflow/02-qiime-temp/ace_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-temp/rarefied_table.qza \
  --p-metric chao1 \
  --o-alpha-diversity dataflow/02-qiime-temp/chao1_vector.qza
  
qiime diversity alpha \
  --i-table dataflow/02-qiime-temp/rarefied_table.qza \
  --p-metric shannon \
  --o-alpha-diversity dataflow/02-qiime-temp/shannon_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-temp/rarefied_table.qza \
  --p-metric simpson_e \
  --o-alpha-diversity dataflow/02-qiime-temp/simpson_e_vector.qza
  
qiime diversity alpha \
  --i-table dataflow/02-qiime-temp/rarefied_table.qza \
  --p-metric simpson \
  --o-alpha-diversity dataflow/02-qiime-temp/simpson_vector.qza



qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-temp/observed_otus_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-observed_otus-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-temp/ace_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-ace-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-temp/chao1_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-chao1-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-temp/shannon_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-shannon-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-temp/simpson_e_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-simpson_e_-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-temp/simpson_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/$metadata \
  --o-visualization dataflow/02-qiime-viz-temp/$outname-simpson-group-significance.qzv







#python snippet

#import os, sys
#import pandas as pd

#df_meta = pd.read_csv('dataflow/00-meta-merge/sample-metadata.tsv', sep = '\t')
#columns = list(df_meta)
#columns.remove('#SampleID')

#for cname in columns:
#	output_f = 'dataflow/02-qiime-viz-merge/beta-sig/weighted-unifrac-' + str(cname) + '-beta-significance.qzv'
#	command = '../bash/q2pipeline/q2_beta_sig.sh' + ' ' + str(cname) + ' ' + output_f 
#	os.system(command)

#for cname in columns:
#	output_f = 'dataflow/02-qiime-viz-merge/beta-sig/unweighted-unifrac-' + str(cname) + '-beta-significance.qzv'
#	command = '../bash/q2pipeline/q2_beta_sig-unweighted.sh' + ' ' + str(cname) + ' ' + output_f
#	os.system(command)

#for cname in columns:
#	output_f = 'dataflow/02-qiime-viz-merge/beta-sig/bray-curtis-' + str(cname) + '-beta-significance.qzv'
#	command = '../bash/q2pipeline/q2_beta_sig-bray.sh' + ' ' + str(cname) + ' ' + output_f
#	os.system(command)