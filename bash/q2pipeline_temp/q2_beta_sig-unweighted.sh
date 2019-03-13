#!/bin/bash

# This script runs paiwise beta significance comparisons and saves the visualizations to
# dataflow/02-qiime-viz/beta-sig/.

colname=$1
fileoutput=$2

qiime diversity beta-group-significance \
  --i-distance-matrix dataflow/02-qiime-temp/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --m-metadata-column $colname \
  --o-visualization $fileoutput \
  --p-pairwise
