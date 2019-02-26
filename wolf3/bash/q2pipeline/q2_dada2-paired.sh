#!/bin/bash

# This script runs DADA2. You need to select the trimming parameters as well as the 
# number of cores that will be used. The DADA2 stats are then made into a visualization,
# so that it can be seen how many reads were removed by DADA2. The files are the renamed.

trimleft_forward=$1
trimleft_reverse=$2
trunclength_forward=$3
trunclength_reverse=$4
numthreads=$5


qiime dada2 denoise-paired \
	--i-demultiplexed-seqs dataflow/02-qiime/demux-trimmed.qza \
	--p-trim-left-f $trimleft_forward \
	--p-trim-left-r $trimleft_reverse \
	--p-trunc-len-f $trunclength_forward \
	--p-trunc-len-r $trunclength_reverse \
	--o-representative-sequences dataflow/02-qiime/rep-seqs-dada2.qza \
	--o-table dataflow/02-qiime/table-dada2.qza \
	--o-denoising-stats dataflow/02-qiime/stats-dada2.qza \
	--p-n-threads $numthreads
	
qiime metadata tabulate \
  --m-input-file dataflow/02-qiime/stats-dada2.qza \
  --o-visualization dataflow/02-qiime-viz/stats-dada2.qzv
  
mv dataflow/02-qiime/rep-seqs-dada2.qza dataflow/02-qiime/rep-seqs.qza
mv dataflow/02-qiime/table-dada2.qza dataflow/02-qiime/table.qza