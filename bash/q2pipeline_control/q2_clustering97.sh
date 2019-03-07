#!/bin/bash

# This clusters sequences to 97% identity and exports the sequences and count table. 

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime-control/table.qza \
  --i-sequences dataflow/02-qiime-control/rep-seqs.qza \
  --p-perc-identity 0.97 \
  --o-clustered-table dataflow/02-qiime-control/table-dn-97.qza \
  --o-clustered-sequences dataflow/02-qiime-control/rep-seqs-dn-97.qza
  
qiime feature-table summarize \
  --i-table dataflow/02-qiime-control/table-dn-97.qza \
  --o-visualization dataflow/02-qiime-viz-control/table-dn-97.qzv 
  
qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime-control/rep-seqs-dn-97.qza \
  --o-visualization dataflow/02-qiime-viz-control/rep-seqs-dn-97.qzv
  
qiime tools export \
  --input-path dataflow/02-qiime-control/table-dn-97.qza \
  --output-path dataflow/03-asv-table-control
  
biom convert -i dataflow/03-asv-table-control/feature-table.biom \
-o dataflow/03-asv-table-control/feature-table-97.txt --to-tsv

rm dataflow/03-asv-table-control/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime-control/rep-seqs-dn-97.qza \
  --output-path dataflow/03-asv-seqs-control
  
mv dataflow/03-asv-seqs-control/dna-sequences.fasta dataflow/03-asv-seqs-control/dna-sequences-97.fasta
  