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
    
mv dataflow/04-tree-merge/tree.nwk dataflow/04-tree-merge/tree-97.nwk