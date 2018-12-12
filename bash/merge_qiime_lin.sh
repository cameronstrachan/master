#!/bin/bash

table1=$1
table2=$2
seqs1=$3
seqs2=$4

conda activate qiime2-2018.11

qiime feature-table merge \
  --i-tables dataflow/02-qiime-merge/$table1 \
  --i-tables dataflow/02-qiime-merge/$table2 \
  --o-merged-table dataflow/02-qiime-merge/table.qza
  
qiime feature-table merge-seqs \
  --i-data dataflow/02-qiime-merge/$seqs1 \
  --i-data dataflow/02-qiime-merge/$seqs2 \
  --o-merged-data dataflow/02-qiime-merge/rep-seqs.qza

#qiime feature-classifier classify-sklearn \
#  --i-classifier ../databases/gg-13-8-99-nb-classifier.qza \
#  --i-reads dataflow/02-qiime-merge/rep-seqs.qza \
#  --o-classification dataflow/02-qiime-merge/gg-taxonomy.qza

#qiime metadata tabulate \
#  --m-input-file dataflow/02-qiime-merge/gg-taxonomy.qza \
#  --o-visualization dataflow/02-qiime-merge/gg-taxonomy.qzv

#qiime feature-table tabulate-seqs \
#  --i-data rep-seqs.qza \
#  --o-visualization rep-seqs.qzv
  
# cluster seqs
qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime-merge/table.qza \
  --i-sequences dataflow/02-qiime-merge/rep-seqs.qza \
  --p-perc-identity 0.99 \
  --o-clustered-table dataflow/02-qiime-merge/table-dn-99.qza \
  --o-clustered-sequences dataflow/02-qiime-merge/rep-seqs-dn-99.qza

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime-merge/table.qza \
  --i-sequences dataflow/02-qiime-merge/rep-seqs.qza \
  --p-perc-identity 0.97 \
  --o-clustered-table dataflow/02-qiime-merge/table-dn-97.qza \
  --o-clustered-sequences dataflow/02-qiime-merge/rep-seqs-dn-97.qza

qiime feature-table summarize \
  --i-table dataflow/02-qiime-merge/table.qza \
  --o-visualization dataflow/02-qiime-merge/table.qzv 

qiime feature-table summarize \
  --i-table dataflow/02-qiime-merge/table-dn-99.qza \
  --o-visualization dataflow/02-qiime-merge/table-dn-99.qzv 

qiime feature-table summarize \
  --i-table dataflow/02-qiime-merge/table-dn-97.qza \
  --o-visualization dataflow/02-qiime-merge/table-dn-97.qzv 

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime-merge/rep-seqs.qza \
  --o-visualization dataflow/02-qiime-merge/rep-seqs.qzv

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime-merge/rep-seqs-dn-99.qza \
  --o-visualization dataflow/02-qiime-merge/rep-seqs-dn-99.qzv

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
  --o-visualization dataflow/02-qiime-merge/rep-seqs-dn-97.qzv

conda deactivate qiime2-2018.11