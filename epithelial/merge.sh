#!/bin/bash

qiime feature-table merge \
  --i-tables dataflow/02-qiime/table_neubauer2018.qza \
  --i-tables dataflow/02-qiime/table_wetzels2017.qza \
  --o-merged-table dataflow/02-qiime/table_neubauer2018_wetzels2017.qza
  
qiime feature-table merge-seqs \
  --i-data dataflow/02-qiime/rep-seqs_neubauer2018.qza \
  --i-data dataflow/02-qiime/rep-seqs_wetzels2017.qza \
  --o-merged-data dataflow/02-qiime/rep-seqs_neubauer2018_wetzels2017.qza

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/table_neubauer2018_wetzels2017.qza \
  --i-sequences dataflow/02-qiime/rep-seqs_neubauer2018_wetzels2017.qza \
  --p-perc-identity 0.99 \
  --o-clustered-table dataflow/02-qiime/table_neubauer2018_wetzels2017-dn-99.qza \
  --o-clustered-sequences dataflow/02-qiime/rep-seqs_neubauer2018_wetzels2017-dn-99.qza  

qiime tools export \
  --input-path dataflow/02-qiime/table_neubauer2018_wetzels2017-dn-99.qza \
  --output-path dataflow/03-asv-table
  
biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/neubauer2018_wetzels2017_99.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs_neubauer2018_wetzels2017-dn-99.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/neubauer2018_wetzels201_99.fasta