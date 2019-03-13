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
  --p-sampling-depth 14000 \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --output-dir dataflow/02-qiime-core-metrics


mv dataflow/02-qiime-core-metrics/*.qza dataflow/02-qiime-merge/
mv dataflow/02-qiime-core-metrics/*.qzv dataflow/02-qiime-viz-merge/
rm -r dataflow/02-qiime-core-metrics/

qiime diversity alpha-group-significance \
  --i-alpha-diversity dataflow/02-qiime-merge/evenness_vector.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/evenness-group-significance.qzv

qiime diversity alpha-rarefaction \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --i-phylogeny dataflow/02-qiime-merge/rooted-no-contam.qza \
  --p-max-depth 14000 \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/alpha-rarefaction-no-contam.qzv

qiime taxa barplot \
  --i-table dataflow/02-qiime-merge/table-dn-97-no-contam.qza \
  --i-taxonomy dataflow/02-qiime-merge/silva-taxonomy-no-contam.qza \
  --m-metadata-file dataflow/00-meta-merge/sample-metadata.tsv \
  --o-visualization dataflow/02-qiime-viz-merge/taxa-bar-plots-no-contam.qzv