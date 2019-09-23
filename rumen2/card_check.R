library(tidyverse)

df_card <- read.delim("~/master/rumen2/dataflow/02-blast-out/stewart2019_mags_genes_300_cp_pathogen_mapped_card.txt", header=FALSE)
colnames(df_card)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_card <- df_card %>%
  filter(pident > 70) %>%
  separate(sseqid, into = c("gene", "organism"), sep = "\\[")

df_card$gene <- gsub("_", "", df_card$gene)
df_card$organism <- gsub("\\]_", "", df_card$organism)
df_card$organism <- gsub("_", " ", df_card$organism)

df_card <- df_card %>%
  separate(gene, into = c('rm', "accession", "ARD", "gene"), sep = "\\|")

df_headers <- read.csv("~/master/rumen2/dataflow/03-analysis/stewart2019_mags_genes_300_cp_mapped_headers.csv")
df_headers$X <- NULL

colnames(df_headers)[1] <- 'qseqid'

test <- inner_join(df_card, df_headers)
