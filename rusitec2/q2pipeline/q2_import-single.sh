#!/bin/bash

qiime tools import \
  --type 'SampleData[SequencesWithQuality]' \
  --input-path dataflow/01-fastq/forward/ \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/forward-demux-trimmed.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/forward-demux-trimmed.qza \
  --o-visualization dataflow/02-qiime-viz/forward-demux-trimmed.qzv
  
#'SampleData[PairedEndSequencesWithQuality]'
#'SampleData[SequencesWithQuality]'