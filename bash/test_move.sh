fileformerge=$1

mv dataflow/02-qiime/rep-seqs.qza dataflow/02-qiime-merge/rep-seqs_$fileformerge.qza
mv dataflow/02-qiime/table.qza $fileformerge dataflow/02-qiime-merge/table_$fileformerge.qza