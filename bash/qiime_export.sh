#!/bin/bash

source activate qiime2-2018.8

# export taxa tables
<<<<<<< HEAD
qiime tools export \
  --input-path dataflow/02-qiime/gg-taxonomy.qza \
  --output-path dataflow/03-asv-table
=======
#qiime tools export \
#  --input-path dataflow/02-qiime/gg-taxonomy.qza \
#  --output-path dataflow/03-asv-table
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

#qiime tools export \
#  --input-path dataflow/02-qiime/silva-taxonomy.qza \
#  --output-path dataflow/03-asv-table

# export otu tables (different clustering)
qiime tools export \
  --input-path dataflow/02-qiime/table.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom -o dataflow/03-asv-table/feature-table-100.txt --to-tsv
rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/table-dn-99.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom -o dataflow/03-asv-table/feature-table-99.txt --to-tsv
rm dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime/table-dn-97.qza \
  --output-path dataflow/03-asv-table

biom convert -i dataflow/03-asv-table/feature-table.biom -o dataflow/03-asv-table/feature-table-97.txt --to-tsv
rm dataflow/03-asv-table/feature-table.biom

# export seqs (different clustering)
qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs.qza \
  --output-path dataflow/03-asv-seqs

mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/dna-sequences-100.fasta

qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs-dn-99.qza \
  --output-path dataflow/03-asv-seqs

mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/dna-sequences-99.fasta

qiime tools export \
  --input-path dataflow/02-qiime/rep-seqs-dn-97.qza \
  --output-path dataflow/03-asv-seqs

mv dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/dna-sequences-97.fasta

source deactivate qiime2-2018.8