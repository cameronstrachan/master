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