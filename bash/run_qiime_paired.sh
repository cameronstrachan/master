#!/bin/bash

<<<<<<< HEAD
lengthcutoff1=$1
lengthcutoff2=$2
numthreads=$3
=======
lengthcutoff1r1=$1
lengthcutoff1r2=$2
lengthcutoff2r1=$3
lengthcutoff2r2=$4
numthreads=$5
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

source activate qiime2-2018.8

# data2
qiime dada2 denoise-paired \
	--i-demultiplexed-seqs dataflow/02-qiime/demux-paired-end.qza \
<<<<<<< HEAD
	--p-trim-left-f $lengthcutoff1 \
	--p-trim-left-r $lengthcutoff1 \
	--p-trunc-len-f $lengthcutoff2 \
	--p-trunc-len-r $lengthcutoff2 \
=======
	--p-trim-left-f $lengthcutoff1r1 \
	--p-trim-left-r $lengthcutoff1r2 \
	--p-trunc-len-f $lengthcutoff2r1 \
	--p-trunc-len-r $lengthcutoff2r2 \
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4
	--o-representative-sequences dataflow/02-qiime/rep-seqs-dada2.qza \
	--o-table dataflow/02-qiime/table-dada2.qza \
	--o-denoising-stats dataflow/02-qiime/stats-dada2.qza \
	--p-n-threads $numthreads
	
qiime metadata tabulate \
  --m-input-file dataflow/02-qiime/stats-dada2.qza \
  --o-visualization dataflow/02-qiime/stats-dada2.qzv
  
# rename otu table and seqs  
mv dataflow/02-qiime/rep-seqs-dada2.qza dataflow/02-qiime/rep-seqs.qza
mv dataflow/02-qiime/table-dada2.qza dataflow/02-qiime/table.qza

# classify seqs
<<<<<<< HEAD
qiime feature-classifier classify-sklearn \
  --i-classifier ../databases/gg-13-8-99-nb-classifier.qza \
  --i-reads dataflow/02-qiime/rep-seqs.qza \
  --o-classification dataflow/02-qiime/gg-taxonomy.qza
=======
#qiime feature-classifier classify-sklearn \
#  --i-classifier ../databases/gg-13-8-99-nb-classifier.qza \
#  --i-reads dataflow/02-qiime/rep-seqs.qza \
#  --o-classification dataflow/02-qiime/gg-taxonomy.qza
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

#qiime feature-classifier classify-sklearn \
#  --i-classifier ../databases/silva-132-99-nb-classifier.qza \
#  --i-reads dataflow/02-qiime/rep-seqs.qza \
#  --o-classification dataflow/02-qiime/silva-taxonomy.qza

<<<<<<< HEAD
qiime metadata tabulate \
  --m-input-file dataflow/02-qiime/gg-taxonomy.qza \
  --o-visualization dataflow/02-qiime/gg-taxonomy.qzv
=======
#qiime metadata tabulate \
#  --m-input-file dataflow/02-qiime/gg-taxonomy.qza \
#  --o-visualization dataflow/02-qiime/gg-taxonomy.qzv
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

#qiime metadata tabulate \
#  --m-input-file dataflow/02-qiime/silva-taxonomy.qza \
#  --o-visualization dataflow/02-qiime/silva-taxonomy.qzv

# cluster seqs
qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/table.qza \
  --i-sequences dataflow/02-qiime/rep-seqs.qza \
  --p-perc-identity 0.99 \
  --o-clustered-table dataflow/02-qiime/table-dn-99.qza \
  --o-clustered-sequences dataflow/02-qiime/rep-seqs-dn-99.qza

qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime/table.qza \
  --i-sequences dataflow/02-qiime/rep-seqs.qza \
  --p-perc-identity 0.97 \
  --o-clustered-table dataflow/02-qiime/table-dn-97.qza \
  --o-clustered-sequences dataflow/02-qiime/rep-seqs-dn-97.qza

qiime feature-table summarize \
  --i-table dataflow/02-qiime/table.qza \
  --o-visualization dataflow/02-qiime/table.qzv 

qiime feature-table summarize \
  --i-table dataflow/02-qiime/table-dn-99.qza \
  --o-visualization dataflow/02-qiime/table-dn-99.qzv 

qiime feature-table summarize \
  --i-table dataflow/02-qiime/table-dn-97.qza \
  --o-visualization dataflow/02-qiime/table-dn-97.qzv 

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime/rep-seqs.qza \
  --o-visualization dataflow/02-qiime/rep-seqs.qzv

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime/rep-seqs-dn-99.qza \
  --o-visualization dataflow/02-qiime/rep-seqs-dn-99.qzv

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime/rep-seqs-dn-97.qza \
  --o-visualization dataflow/02-qiime/rep-seqs-dn-97.qzv

source deactivate qiime2-2018.8
