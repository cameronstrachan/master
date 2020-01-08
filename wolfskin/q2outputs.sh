#!/bin/bash

qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences dataflow/02-qiime/rep-seqs-decontam.qza \
  --o-alignment dataflow/02-qiime/aligned-rep-seqs-decontam.qza \
  --o-masked-alignment dataflow/02-qiime/masked-aligned-rep-seqs-decontam.qza \
  --o-tree dataflow/02-qiime/unrooted-tree-decontam.qza \
  --o-rooted-tree dataflow/02-qiime/rooted-decontam.qza

qiime tools export \
    --input-path dataflow/02-qiime/rooted-decontam.qza \
    --output-path dataflow/03-asv-seqs

mv dataflow/03-asv-seqs/tree.nwk dataflow/03-asv-seqs/tree-decontam.nwk

qiime feature-table summarize \
  --i-table dataflow/02-qiime/table-decontam.qza \
  --o-visualization dataflow/02-qiime-viz/table-decontam.qzv \
  --m-sample-metadata-file dataflow/00-meta/sample-metadata.tsv

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny dataflow/02-qiime/rooted-decontam.qza \
  --i-table dataflow/02-qiime/table-decontam.qza \
  --p-sampling-depth 14000 \
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
  --i-table dataflow/02-qiime/table-decontam.qza \
  --i-phylogeny dataflow/02-qiime/rooted-decontam.qza \
  --p-max-depth 14000 \
  --m-metadata-file dataflow/00-meta/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz/alpha-rarefaction-decontam.qzv

qiime diversity beta-group-significance \
    --i-distance-matrix dataflow/02-qiime/bray_curtis_distance_matrix.qza \
    --m-metadata-file dataflow/00-meta/sample-metadata.tsv \
    --m-metadata-column SAMPLEtype \
    --o-visualization dataflow/02-qiime-viz/beta-sig-bray.qzv \
    --p-pairwise
