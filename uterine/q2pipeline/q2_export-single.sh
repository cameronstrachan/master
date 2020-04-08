#!/bin/bash

# asvs
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

# 99
qiime tools export \
  --input-path dataflow/02-qiime/forward-table-dn-99.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/forward-feature-table-99.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/forward-rep-seqs-dn-99.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/forward-dna-sequences-99.fasta

# 98
qiime tools export \
  --input-path dataflow/02-qiime/forward-table-dn-98.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/forward-feature-table-98.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/forward-rep-seqs-dn-98.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/forward-dna-sequences-98.fasta

# 97
qiime tools export \
  --input-path dataflow/02-qiime/forward-table-dn-97.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/forward-feature-table-97.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/forward-rep-seqs-dn-97.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/forward-dna-sequences-97.fasta

# 96
qiime tools export \
  --input-path dataflow/02-qiime/forward-table-dn-96.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/forward-feature-table-96.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/forward-rep-seqs-dn-96.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/forward-dna-sequences-96.fasta

# 95
qiime tools export \
  --input-path dataflow/02-qiime/forward-table-dn-95.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/forward-feature-table-95.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/forward-rep-seqs-dn-95.qza \
  --output-path dataflow/03-asv-seqs
  
mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/forward-dna-sequences-95.fasta
