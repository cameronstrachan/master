#!/bin/bash

inputfolder=$1

source activate qiime2-2018.8

# import
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path $inputfolder \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/demux-paired-end.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/demux-paired-end.qza \
  --o-visualization dataflow/02-qiime/demux-paired-end.qzv

source deactivate qiime2-2018.8