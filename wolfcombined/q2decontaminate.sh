#!/bin/bash

biom convert -i dataflow/03-asv-table/feature-table-decontam.txt -o dataflow/03-asv-table/feature-table-decontam.biom --table-type="OTU table" --to-hdf5

qiime tools import \
	--input-path dataflow/03-asv-table/feature-table-decontam.biom \
	--type "FeatureTable[Frequency]" \
	--output-path dataflow/02-qiime/table-decontam.qza

rm dataflow/03-asv-table/feature-table-decontam.biom

qiime tools export \
  --input-path dataflow/02-qiime/table-decontam.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom \
-o dataflow/03-asv-table/feature-table-decontam.txt --to-tsv

rm dataflow/03-asv-table/feature-table.biom

qiime feature-table filter-seqs \
	--i-data dataflow/02-qiime/rep-seqs.qza \
	--i-table dataflow/02-qiime/table-decontam.qza \
	--o-filtered-data dataflow/02-qiime/rep-seqs-decontam.qza

qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs-decontam.qza \
  --output-path dataflow/03-asv-seqs

mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/dna-sequences-decontam.fasta
