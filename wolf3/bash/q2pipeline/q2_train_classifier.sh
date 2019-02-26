#!/bin/bash

# This script trains a classifier to the give primers. 

forward_primer=$1
reverse_primer=$2

qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path dataflow/00-databases/silva_132_99_16S.fna \
  --output-path dataflow/02-qiime/silva_132_99_16S.qza

qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path dataflow/00-databases/taxonomy_7_levels.txt \
  --output-path dataflow/02-qiime/silva-ref-taxonomy.qza

qiime feature-classifier extract-reads \
  --i-sequences dataflow/02-qiime/silva_132_99_16S.qza \
  --p-f-primer $forward_primer \
  --p-r-primer $reverse_primer \
  --p-min-length 100 \
  --p-max-length 400 \
  --o-reads dataflow/02-qiime/silva_132_99_16S_trimmed.qza

qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads dataflow/02-qiime/silva_132_99_16S_trimmed.qza \
  --i-reference-taxonomy dataflow/02-qiime/silva-ref-taxonomy.qza \
  --o-classifier dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza