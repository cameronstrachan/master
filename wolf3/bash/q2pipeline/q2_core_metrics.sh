#!/bin/bash

# This script runs various standard analysis from qiime2 and outputs all the 
# visualizations to dataflow/02-qiime-viz/.

sample_depth=$1

qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences dataflow/02-qiime/rep-seqs-dn-97.qza \
  --o-alignment dataflow/02-qiime/aligned-rep-seqs-dn-97.qza \
  --o-masked-alignment dataflow/02-qiime/masked-aligned-rep-seqs-dn-97.qza \
  --o-tree dataflow/02-qiime/unrooted-tree.qza \
  --o-rooted-tree dataflow/02-qiime/rooted-tree.qza

qiime feature-table summarize \
  --i-table dataflow/02-qiime/table-dn-97.qza \
  --o-visualization dataflow/02-qiime-viz/table-dn-97.qzv \
  --m-sample-metadata-file dataflow/00-meta/sample-metadata.tsv

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny dataflow/02-qiime/rooted-tree.qza \
  --i-table dataflow/02-qiime/table-dn-97.qza \
  --p-sampling-depth $sample_depth \
  --m-metadata-file dataflow/00-meta/sample-metadata.tsv \
  --output-dir dataflow/02-qiime-core-metrics

mv dataflow/02-qiime-core-metrics/*.qza dataflow/02-qiime/
mv dataflow/02-qiime-core-metrics/*.qzv dataflow/02-qiime-viz/
rm -r dataflow/02-qiime-core-metrics/

qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime/evenness_vector.qza \
  --m-metadata-file dataflow/00-meta/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz/evenness-group-significance.qzv

qiime diversity alpha-rarefaction \
  --i-table dataflow/02-qiime/table-dn-97.qza \
  --i-phylogeny dataflow/02-qiime/rooted-tree.qza \
  --p-max-depth 10000 \
  --m-metadata-file dataflow/00-meta/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz/alpha-rarefaction.qzv