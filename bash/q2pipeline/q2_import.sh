#!/bin/bash

paired_or_not_paired=$1

qiime tools import \
  --type $paired_or_not_paired \
  --input-path dataflow/01-fastq/ \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/demux-trimmed.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/demux-trimmed.qza \
  --o-visualization dataflow/02-qiime-viz/demux-trimmed.qzv
  
#'SampleData[PairedEndSequencesWithQuality]'
#'SampleData[SequencesWithQuality]'