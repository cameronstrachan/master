#!/bin/bash

source activate qiime2-2018.8

qiime tools export \
  --input-path dataflow/02-qiime/table.qza \
  --output-path dataflow/03-asv-table
  
qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs.qza \
  --output-path dataflow/03-asv-seqs

biom convert -i dataflow/03-asv-table/feature-table.biom -o dataflow/03-asv-table/feature-table.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

source deactivate qiime2-2018.8