#!/bin/bash

# This clusters sequences to 99% identity and exports the sequences and count table. 

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/table.qza \
  --i-sequences dataflow/02-qiime/rep-seqs.qza \
  --p-perc-identity 0.99 \
  --o-clustered-table dataflow/02-qiime/table-dn-99.qza \
  --o-clustered-sequences dataflow/02-qiime/rep-seqs-dn-99.qza
  
qiime feature-table summarize \
  --i-table dataflow/02-qiime/table-dn-99.qza \
  --o-visualization dataflow/02-qiime-viz/table-dn-99.qzv 
  
qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime/rep-seqs-dn-99.qza \
  --o-visualization dataflow/02-qiime-viz/rep-seqs-dn-99.qzv
  
qiime tools export \
  --input-path dataflow/02-qiime/table-dn-99.qza \
  --output-path dataflow/03-asv-table
  
biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/feature-table-99.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs-dn-99.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/dna-sequences-99.fasta
  