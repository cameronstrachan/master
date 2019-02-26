#!/bin/bash

# This script imports data from dataflow/01-fastq/trimmed/ into a .qza file and then
# creates the .qzv visualization (dataflow/02-qiime-viz/demux-paired-end.qzv) for looking 
# at the sequencing quality. This visualization can be viewed at https://view.qiime2.org/
# and should be used to decide on any trimming to the sequences. The data being imported
# should be demultiplexed with adapter, primers etc. removed. 

paired_or_not_paired=$1

qiime tools import \
  --type $paired_or_not_paired \
  --input-path dataflow/01-fastq/trimmed/ \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path dataflow/02-qiime/demux-trimmed.qza
  
qiime demux summarize \
  --i-data dataflow/02-qiime/demux-paired-end.qza \
  --o-visualization dataflow/02-qiime-viz/demux-trimmed.qzv
  
  
#'SampleData[PairedEndSequencesWithQuality]'
#'SampleData[SequencesWithQuality]'