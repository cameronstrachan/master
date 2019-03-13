qiime feature-table merge \
  --i-tables milk/dataflow/02-qiime/table.qza \
  --i-tables milk-control/dataflow/02-qiime/table.qza \
  --o-merged-table milk-merge/dataflow/02-qiime/table.qza
  
qiime feature-table merge-seqs \
  --i-data milk/dataflow/02-qiime/rep-seqs.qza \
  --i-data milk-control/dataflow/02-qiime/rep-seqs.qza \
  --o-merged-data milk-merge/dataflow/02-qiime/rep-seqs.qza
  
qiime vsearch cluster-features-de-novo \
  --i-table milk-merge/dataflow/02-qiime/table.qza \
  --i-sequences milk-merge/dataflow/02-qiime/rep-seqs.qza \
  --p-perc-identity 0.97 \
  --o-clustered-table milk-merge/dataflow/02-qiime/table-dn-97.qza \
  --o-clustered-sequences milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza
  
qiime feature-table summarize \
  --i-table milk-merge/dataflow/02-qiime/table-dn-97.qza \
  --o-visualization milk-merge/dataflow/02-qiime-viz/table-dn-97.qzv 
  
qiime feature-table tabulate-seqs \
  --i-data milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza \
  --o-visualization milk-merge/dataflow/02-qiime-viz/rep-seqs-dn-97.qzv
  
qiime tools export \
  --input-path milk-merge/dataflow/02-qiime/table-dn-97.qza \
  --output-path milk-merge/dataflow/03-asv-table
  
biom convert -i milk-merge/dataflow/03-asv-table/feature-table.biom \
-o milk-merge/dataflow/03-asv-table/feature-table-97.txt --to-tsv

rm milk-merge/dataflow/03-asv-table/feature-table.biom

qiime tools export \
  --input-path milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza \
  --output-path milk-merge/dataflow/03-asv-seqs
  
mv milk-merge/dataflow/03-asv-seqs/dna-sequences.fasta dataflow/03-asv-seqs/dna-sequences-97.fasta

qiime feature-classifier classify-sklearn \
  --i-classifier milk-merge/dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza \
  --i-reads milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza \
  --p-n-jobs -1 \
  --o-classification milk-merge/dataflow/02-qiime/silva-taxonomy.qza

qiime tools export \
    --input-path milk-merge/dataflow/02-qiime/silva-taxonomy.qza \
    --output-path milk-merge/dataflow/03-asv-table
  
mv milk-merge/dataflow/03-asv-table/taxonomy.tsv milk-merge/dataflow/03-asv-table/taxonomy-complete.tsv
  
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza \
  --o-alignment milk-merge/dataflow/02-qiime/aligned-rep-seqs-dn-97.qza \
  --o-masked-alignment milk-merge/dataflow/02-qiime/masked-aligned-rep-seqs-dn-97.qza \
  --o-tree milk-merge/dataflow/02-qiime/unrooted-tree.qza \
  --o-rooted-tree milk-merge/dataflow/02-qiime/rooted-tree.qza
  
qiime tools export \
    --input-path milk-merge/dataflow/02-qiime/rooted-tree.qza \
    --output-path milk-merge/dataflow/04-tree
    
qiime feature-classifier classify-sklearn \
  --i-classifier milk-merge/dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza \
  --i-reads milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza \
  --p-n-jobs -10 \
  --o-classification milk-merge/dataflow/02-qiime/silva-taxonomy.qza

qiime tools export \
    --input-path milk-merge/dataflow/02-qiime/silva-taxonomy.qza \
    --output-path milk-merge/dataflow/03-asv-table
  
biom convert -i milk-merge/dataflow/03-asv-table/feature-table-no-contam.txt -o milk-merge/dataflow/03-asv-table/feature-table-no-contam.biom --table-type="OTU table" --to-hdf5
  
qiime tools import \
	--input-path milk-merge/dataflow/03-asv-table/feature-table-no-contam.biom \
	--type "FeatureTable[Frequency]" \
	--output-path milk-merge/dataflow/02-qiime/table-dn-97-no-contam.qza

qiime feature-table filter-seqs \
	--i-data milk-merge/dataflow/02-qiime/rep-seqs-dn-97.qza \
	--i-table milk-merge/dataflow/02-qiime/table-dn-97-no-contam.qza \
	--o-filtered-data milk-merge/dataflow/02-qiime/rep-seqs-dn-97-no-contam.qza

qiime feature-classifier classify-sklearn \
  --i-classifier milk-merge/dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza \
  --i-reads milk-merge/dataflow/02-qiime/rep-seqs-dn-97-no-contam.qza \
  --p-n-jobs -1 \
  --o-classification milk-merge/dataflow/02-qiime/silva-taxonomy-no-contam.qza



qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences milk-merge/dataflow/02-qiime/rep-seqs-dn-97-no-contam.qza \
  --o-alignment milk-merge/dataflow/02-qiime/aligned-rep-seqs-dn-97-no-contam.qza \
  --o-masked-alignment milk-merge/dataflow/02-qiime/masked-aligned-rep-seqs-dn-97-no-contam.qza \
  --o-tree milk-merge/dataflow/02-qiime/unrooted-tree-no-contam.qza \
  --o-rooted-tree milk-merge/dataflow/02-qiime/rooted-no-contam.qza

qiime feature-table summarize \
  --i-table milk-merge/dataflow/02-qiime/table-dn-97-no-contam.qza \
  --o-visualization milk-merge/dataflow/02-qiime-viz/table-dn-97-no-contam.qzv \
  --m-sample-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny milk-merge/dataflow/02-qiime/rooted-no-contam.qza \
  --i-table milk-merge/dataflow/02-qiime/table-dn-97-no-contam.qza \
  --p-sampling-depth 4000 \
  --m-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv \
  --output-dir milk-merge/dataflow/02-qiime-core-metrics

mv milk-merge/dataflow/02-qiime-core-metrics/*.qza milk-merge/dataflow/02-qiime/
mv milk-merge/dataflow/02-qiime-core-metrics/*.qzv milk-merge/dataflow/02-qiime-viz/
rm -r milk-merge/dataflow/02-qiime-core-metrics/

qiime diversity alpha-group-significance \
  --i-alpha-diversity milk-merge/dataflow/02-qiime/evenness_vector.qza \
  --m-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv \
  --o-visualization milk-merge/dataflow/02-qiime-viz/evenness-group-significance.qzv

qiime diversity alpha-rarefaction \
  --i-table milk-merge/dataflow/02-qiime/table-dn-97-no-contam.qza \
  --i-phylogeny milk-merge/dataflow/02-qiime/rooted-no-contam.qza \
  --p-max-depth 4000 \
  --m-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv \
  --o-visualization milk-merge/dataflow/02-qiime-viz/alpha-rarefaction-no-contam.qzv

qiime taxa barplot \
  --i-table milk-merge/dataflow/02-qiime/table-dn-97-no-contam.qza \
  --i-taxonomy milk-merge/dataflow/02-qiime/silva-taxonomy-no-contam.qza \
  --m-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv \
  --o-visualization milk-merge/dataflow/02-qiime-viz/taxa-bar-plots-no-contam.qzv


qiime diversity beta-group-significance \
  --i-distance-matrix milk-merge/dataflow/02-qiime/weighted_unifrac_distance_matrix.qza \
  --m-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv \
  --m-metadata-column Category \
  --o-visualization milk-merge/dataflow/02-qiime-viz/category-pairwise-beta-weighted.qzv \
  --p-pairwise


qiime diversity beta-group-significance \
  --i-distance-matrix milk-merge/dataflow/02-qiime/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file milk-merge/dataflow/00-meta/sample-metadata.tsv \
  --m-metadata-column Category \
  --o-visualization milk-merge/dataflow/02-qiime-viz/category-pairwise-beta-unweighted.qzv \
  --p-pairwise



