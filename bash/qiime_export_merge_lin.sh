#!/bin/bash

# export taxa tables
#qiime tools export \
#  --input-path dataflow/02-qiime-merge/gg-taxonomy.qza \
#  --output-path dataflow/03-asv-table-merge

#qiime tools export \
#  --input-path dataflow/02-qiime-merge/silva-taxonomy.qza \
#  --output-path dataflow/03-asv-table-merge

# export otu tables (different clustering)
qiime tools export \
  --input-path dataflow/02-qiime-merge/table.qza \
  --output-path dataflow/03-asv-table-merge

biom convert -i dataflow/03-asv-table-merge/feature-table.biom -o dataflow/03-asv-table-merge/feature-table-100.txt --to-tsv
rm dataflow/03-asv-table-merge/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime-merge/table-dn-99.qza \
  --output-path dataflow/03-asv-table-merge

biom convert -i dataflow/03-asv-table-merge/feature-table.biom -o dataflow/03-asv-table-merge/feature-table-99.txt --to-tsv
rm dataflow/03-asv-table-merge/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime-merge/table-dn-98.qza \
  --output-path dataflow/03-asv-table-merge

biom convert -i dataflow/03-asv-table-merge/feature-table.biom -o dataflow/03-asv-table-merge/feature-table-98.txt --to-tsv
rm dataflow/03-asv-table-merge/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime-merge/table-dn-97.qza \
  --output-path dataflow/03-asv-table-merge

biom convert -i dataflow/03-asv-table-merge/feature-table.biom -o dataflow/03-asv-table-merge/feature-table-97.txt --to-tsv
rm dataflow/03-asv-table-merge/feature-table.biom

# export seqs (different clustering)
qiime tools export \
  --input-path dataflow/02-qiime-merge/rep-seqs.qza \
  --output-path dataflow/03-asv-seqs-merge

mv dataflow/03-asv-seqs-merge/dna-sequences.fasta dataflow/03-asv-seqs-merge/dna-sequences-100.fasta

qiime tools export \
  --input-path dataflow/02-qiime-merge/rep-seqs-dn-99.qza \
  --output-path dataflow/03-asv-seqs-merge

mv dataflow/03-asv-seqs-merge/dna-sequences.fasta dataflow/03-asv-seqs-merge/dna-sequences-99.fasta

qiime tools export \
  --input-path dataflow/02-qiime-merge/rep-seqs-dn-98.qza \
  --output-path dataflow/03-asv-seqs-merge

mv dataflow/03-asv-seqs-merge/dna-sequences.fasta dataflow/03-asv-seqs-merge/dna-sequences-98.fasta

qiime tools export \
  --input-path dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
  --output-path dataflow/03-asv-seqs-merge

mv dataflow/03-asv-seqs-merge/dna-sequences.fasta dataflow/03-asv-seqs-merge/dna-sequences-97.fasta
