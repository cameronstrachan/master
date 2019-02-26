#!/bin/bash

# This script classifies the sequences. 

qiime feature-classifier classify-sklearn \
  --i-classifier dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza \
  --i-reads dataflow/02-qiime/rep-seqs-dn-97.qza \
  --p-n-jobs -5 \
  --o-classification dataflow/02-qiime/silva-taxonomy.qza

qiime tools export \
    --input-path dataflow/02-qiime/silva-taxonomy.qza \
    --output-path dataflow/03-asv-table