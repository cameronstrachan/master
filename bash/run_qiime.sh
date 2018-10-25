#!/bin/bash

source activate qiime2-2018.8

qiime tools import \
  --type 'SampleData[SequencesWithQuality]' \
  --input-path dataflow/01-fastq \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/demux-single-end.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/demux-single-end.qza \
  --o-visualization dataflow/02-qiime/demux-single-end.qzv
  
qiime dada2 denoise-single \
  --i-demultiplexed-seqs dataflow/02-qiime/demux-single-end.qza \
  --p-trim-left 1 \
  --p-trunc-len 525 \
  --o-representative-sequences dataflow/02-qiime/rep-seqs-dada2.qza \
  --o-table dataflow/02-qiime/table-dada2.qza \
  --o-denoising-stats dataflow/02-qiime/stats-dada2.qza
  
qiime metadata tabulate \
  --m-input-file dataflow/02-qiime/stats-dada2.qza \
  --o-visualization dataflow/02-qiime/stats-dada2.qzv
  
mv dataflow/02-qiime/rep-seqs-dada2.qza dataflow/02-qiime/rep-seqs.qza
mv dataflow/02-qiime/table-dada2.qza dataflow/02-qiime/table.qza

qiime feature-table summarize \
  --i-table dataflow/02-qiime/table.qza \
  --o-visualization dataflow/02-qiime/table.qzv 

qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime/rep-seqs.qza \
  --o-visualization dataflow/02-qiime/rep-seqs.qzv
  
source deactivate qiime2-2018.8
