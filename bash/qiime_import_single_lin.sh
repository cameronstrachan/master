#!/bin/bash

inputfolder=$1


qiime tools import \
  --type 'SampleData[SequencesWithQuality]' \
  --input-path $inputfolder \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/demux-single-end.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/demux-single-end.qza \
  --o-visualization dataflow/02-qiime/demux-single-end.qzv
  