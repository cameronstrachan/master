qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-metric observed_otus \
  --o-alpha-diversity dataflow/02-qiime-merge/observed_otus_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-metric ace \
  --o-alpha-diversity dataflow/02-qiime-merge/ace_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-metric chao1 \
  --o-alpha-diversity dataflow/02-qiime-merge/chao1_vector.qza
  
qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-metric shannon \
  --o-alpha-diversity dataflow/02-qiime-merge/shannon_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-metric simpson_e \
  --o-alpha-diversity dataflow/02-qiime-merge/simpson_e_vector.qza
  
qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-metric simpson \
  --o-alpha-diversity dataflow/02-qiime-merge/simpson_vector.qza



qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/observed_otus_vector.qzaa \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/observed_otus-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity ddataflow/02-qiime-merge/ace_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/ace-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/chao1_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/chao1-group-significance.qzv
  
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/shannon_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/shannon-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/simpson_e_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/simpson_e_-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/simpson_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/simpson-group-significance.qzv