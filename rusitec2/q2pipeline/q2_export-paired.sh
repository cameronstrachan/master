#!/bin/bash

qiime tools export \
  --input-path dataflow/02-qiime/paired-table.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/paired-feature-table.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/paired-rep-seqs.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/paired-dna-sequences.fasta