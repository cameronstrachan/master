library(tidyverse)

df_blast <- read.delim("~/master/epithelial/dataflow/02-blast/sanger_core_map.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast <- df_blast %>%
  filter(pident > 95 & length > 170) %>%
  select(qseqid, sseqid, pident, length) 
  
