#!/bin/bash

qiime tools export \
  --input-path dataflow/02-qiime/forward-table.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/forward-feature-table.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/forward-rep-seqs.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/forward-dna-sequences.fasta

  
qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/forward-table.qza \
  --i-sequences dataflow/02-qiime/forward-rep-seqs.qza \
  --p-perc-identity 0.99 \
  --o-clustered-table dataflow/02-qiime/forward-table-dn-99.qza \
  --o-clustered-sequences dataflow/02-qiime/forward-rep-seqs-dn-99.qza

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/forward-table.qza \
  --i-sequences dataflow/02-qiime/forward-rep-seqs.qza \
  --p-perc-identity 0.98 \
  --o-clustered-table dataflow/02-qiime/forward-table-dn-98.qza \
  --o-clustered-sequences dataflow/02-qiime/forward-rep-seqs-dn-98.qza

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/forward-table.qza \
  --i-sequences dataflow/02-qiime/forward-rep-seqs.qza \
  --p-perc-identity 0.97 \
  --o-clustered-table dataflow/02-qiime/forward-table-dn-97.qza \
  --o-clustered-sequences dataflow/02-qiime/forward-rep-seqs-dn-97.qza
    
qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/forward-table.qza \
  --i-sequences dataflow/02-qiime/forward-rep-seqs.qza \
  --p-perc-identity 0.96 \
  --o-clustered-table dataflow/02-qiime/forward-table-dn-96.qza \
  --o-clustered-sequences dataflow/02-qiime/forward-rep-seqs-dn-96.qza
  
  qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/forward-table.qza \
  --i-sequences dataflow/02-qiime/forward-rep-seqs.qza \
  --p-perc-identity 0.95 \
  --o-clustered-table dataflow/02-qiime/forward-table-dn-95.qza \
  --o-clustered-sequences dataflow/02-qiime/forward-rep-seqs-dn-95.qza
    

  
