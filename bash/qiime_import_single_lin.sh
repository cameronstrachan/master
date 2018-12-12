#!/bin/bash

inputfolder=$1

conda activate qiime2-2018.11

qiime tools import \
  --type 'SampleData[SequencesWithQuality]' \
  --input-path $inputfolder \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/demux-single-end.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/demux-single-end.qza \
  --o-visualization dataflow/02-qiime/demux-single-end.qzv
  
conda deactivate qiime2-2018.11