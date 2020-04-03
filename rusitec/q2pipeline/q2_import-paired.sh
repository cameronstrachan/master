#!/bin/bash

qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path dataflow/01-fastq/forward/ \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/paired-demux-trimmed.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/forward-demux-trimmed.qza \
  --o-visualization dataflow/02-qiime-viz/paired-demux-trimmed.qzv
  
#'SampleData[PairedEndSequencesWithQuality]'
#'SampleData[SequencesWithQuality]'