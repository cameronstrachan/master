qiime feature-table merge \
  --i-tables dataflow/02-qiime/table.qza \
  --i-tables dataflow/02-qiime-control/table.qza \
  --o-merged-table dataflow/02-qiime-merge/table.qza
  
qiime feature-table merge-seqs \
  --i-data dataflow/02-qiime/rep-seqs.qza \
  --i-data dataflow/02-qiime-control/rep-seqs.qza \
  --o-merged-data dataflow/02-qiime-merge/rep-seqs.qza
  
qiime vsearch cluster-features-de-novo \
  --i-table dataflow/02-qiime-merge/table.qza \
  --i-sequences dataflow/02-qiime-merge/rep-seqs.qza \
  --p-perc-identity 0.97 \
  --o-clustered-table dataflow/02-qiime-merge/table-dn-97.qza \
  --o-clustered-sequences dataflow/02-qiime-merge/rep-seqs-dn-97.qza
  
qiime feature-table summarize \
  --i-table dataflow/02-qiime-merge/table-dn-97.qza \
  --o-visualization dataflow/02-qiime-viz-merge/table-dn-97.qzv 
  
qiime feature-table tabulate-seqs \
  --i-data dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
  --o-visualization dataflow/02-qiime-viz-merge/rep-seqs-dn-97.qzv
  
qiime tools export \
  --input-path dataflow/02-qiime-merge/table-dn-97.qza \
  --output-path dataflow/03-asv-table-merge
  
biom convert -i dataflow/03-asv-table-merge/feature-table.biom \
-o dataflow/03-asv-table-merge/feature-table-97.txt --to-tsv

rm dataflow/03-asv-table-merge/feature-table.biom

qiime tools export \
  --input-path dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
  --output-path dataflow/03-asv-seqs-merge
  
mv dataflow/03-asv-seqs-merge/dna-sequences.fasta dataflow/03-asv-seqs-merge/dna-sequences-97.fasta

qiime feature-classifier classify-sklearn \
  --i-classifier dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza \
  --i-reads dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
  --p-n-jobs -10 \
  --o-classification dataflow/02-qiime-merge/silva-taxonomy.qza

qiime tools export \
    --input-path dataflow/02-qiime-merge/silva-taxonomy.qza \
    --output-path dataflow/03-asv-table-merge
  
mv dataflow/03-asv-table-merge/taxonomy.tsv dataflow/03-asv-table-merge/taxonomy-complete.tsv
 
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
  --o-alignment dataflow/02-qiime-merge/aligned-rep-seqs-dn-97.qza \
  --o-masked-alignment dataflow/02-qiime-merge/masked-aligned-rep-seqs-dn-97.qza \
  --o-tree dataflow/02-qiime-merge/unrooted-tree.qza \
  --o-rooted-tree dataflow/02-qiime-merge/rooted-tree.qza
  
qiime tools export \
    --input-path dataflow/02-qiime-merge/rooted-tree.qza \
    --output-path dataflow/04-tree-merge
    
Rscript src/R/decontam.R
  
biom convert -i dataflow/03-asv-table-merge/feature-table-no-contam.txt -o dataflow/03-asv-table-merge/feature-table-no-contam.biom --table-type="OTU table" --to-hdf5
  
qiime tools import \
	--input-path dataflow/03-asv-table-merge/feature-table-no-contam.biom \
	--type "FeatureTable[Frequency]" \
	--output-path dataflow/02-qiime-merge/table-dn-97-no-contam.qza

qiime tools export \
  --input-path dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --output-path dataflow/03-asv-table-merge
  
biom convert -i dataflow/03-asv-table-merge/feature-table.biom \
-o dataflow/03-asv-table-merge/feature-table-97-no-contam.txt --to-tsv

rm dataflow/03-asv-table-merge/feature-table.biom

qiime feature-table filter-seqs \
	--i-data dataflow/02-qiime-merge/rep-seqs-dn-97.qza \
	--i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
	--o-filtered-data dataflow/02-qiime-merge/rep-seqs-dn-97-no-contam.qza

qiime tools export \
  --input-path dataflow/02-qiime-merge/rep-seqs-dn-97-no-contam.qza \
  --output-path dataflow/03-asv-seqs-merge
  
mv dataflow/03-asv-seqs-merge/dna-sequences.fasta dataflow/03-asv-seqs-merge/dna-sequences-97-no-contam.fasta

qiime feature-classifier classify-sklearn \
  --i-classifier dataflow/02-qiime/silva_132_99_16S_trimmed_classifier.qza \
  --i-reads dataflow/02-qiime-merge/rep-seqs-dn-97-no-contam.qza \
  --p-n-jobs -10 \
  --o-classification dataflow/02-qiime-merge/silva-taxonomy-no-contam.qza

qiime tools export \
    --input-path dataflow/02-qiime-merge/silva-taxonomy-no-contam.qza \
    --output-path dataflow/03-asv-table-merge

mv dataflow/03-asv-table-merge/taxonomy.tsv dataflow/03-asv-table-merge/taxonomy-no-contam.tsv

qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences dataflow/02-qiime-merge/rep-seqs-dn-97-no-contam.qza \
  --o-alignment dataflow/02-qiime-merge/aligned-rep-seqs-dn-97-no-contam.qza \
  --o-masked-alignment dataflow/02-qiime-merge/masked-aligned-rep-seqs-dn-97-no-contam.qza \
  --o-tree dataflow/02-qiime-merge/unrooted-tree-no-contam.qza \
  --o-rooted-tree dataflow/02-qiime-merge/rooted-no-contam.qza

#qiime tools export \
#    --input-path dataflow/02-qiime-merge/rooted-no-contam.qza \
#    --output-path dataflow/04-tree-merge

qiime feature-table summarize \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --o-visualization dataflow/02-qiime-viz-merge/table-dn-97-no-contam.qzv \
  --m-sample-metadata-file dataflow/00-meta-merge/sample-metadata.tsv

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny dataflow/02-qiime-merge/rooted-no-contam.qza \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --p-sampling-depth 4000 \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --output-dir dataflow/02-qiime-core-metrics

mv dataflow/02-qiime-core-metrics/*.qza dataflow/02-qiime/
mv dataflow/02-qiime-core-metrics/*.qzv dataflow/02-qiime-viz/
rm -r dataflow/02-qiime-core-metrics/

qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/evenness_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/evenness-group-significance.qzv

qiime diversity alpha-rarefaction \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --i-phylogeny dataflow/02-qiime-merge/rooted-no-contam.qza \
  --p-max-depth 4000 \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/alpha-rarefaction-no-contam.qzv

qiime taxa barplot \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --i-taxonomy mdataflow/02-qiime-merge/silva-taxonomy-no-contam.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/taxa-bar-plots-no-contam.qzv

qiime diversity beta-group-significance \
  --i-distance-matrix dataflow/02-qiime-merge/weighted_unifrac_distance_matrix.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --m-metadata-column Category \
  --o-visualization dataflow/02-qiime-viz-merge/category-pairwise-beta-weighted.qzv \
  --p-pairwise

qiime diversity beta-group-significance \
  --i-distance-matrix dataflow/02-qiime-merge/unweighted_unifrac_distance_matrix.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --m-metadata-column Category \
  --o-visualization dataflow/02-qiime-viz-merge/category-pairwise-beta-unweighted.qzv \
  --p-pairwise


### more alpha metrics

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/rarefied_table.qza \
  --p-metric observed_otus \
  --o-alpha-diversity dataflow/02-qiime-merge/observed_otus_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/rarefied_table.qza \
  --p-metric ace \
  --o-alpha-diversity dataflow/02-qiime-merge/ace_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/rarefied_table.qza \
  --p-metric chao1 \
  --o-alpha-diversity dataflow/02-qiime-merge/chao1_vector.qza
  
qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/rarefied_table.qza \
  --p-metric shannon \
  --o-alpha-diversity dataflow/02-qiime-merge/shannon_vector.qza

qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/rarefied_table.qza \
  --p-metric simpson_e \
  --o-alpha-diversity dataflow/02-qiime-merge/simpson_e_vector.qza
  
qiime diversity alpha \
  --i-table dataflow/02-qiime-merge/rarefied_table.qza \
  --p-metric simpson \
  --o-alpha-diversity dataflow/02-qiime-merge/simpson_vector.qza



qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/observed_otus_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/observed_otus-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/ace_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/ace-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/chao1_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/chao1-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/shannon_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/shannon-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/simpson_e_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/simpson_e_-group-significance.qzv
  
qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/simpson_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/simpson-group-significance.qzv


