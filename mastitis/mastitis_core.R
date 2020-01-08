library(tidyverse)
library(stringi)

df_blast <- read.delim("~/master/mastitis/dataflow/03-tables/mastitis_core.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast$qseqid <- as.character(df_blast$qseqid)
df_blast$sseqid <- as.character(df_blast$sseqid)

df_meta <- read.csv("~/master/mastitis/dataflow/00-meta/complete_genomes.csv")
df_meta$accession <- as.character(df_meta$accession)

accessions <- unique(df_meta$accession)

df_blast <- df_blast %>% 
  mutate(cov = length / qlen) %>%
  filter(cov > 0.90) %>%
  filter(pident > 70) %>%
  separate(qseqid, into = c('qseqid_prefix', 'qseqid_acc', 'qseqid_gene_num'), sep = '_', remove = FALSE) %>%
  separate(sseqid, into = c('sseqid_prefix', 'sseqid_acc', 'sseqid_gene_num'), sep = '_', remove = FALSE) %>%
  unite(qseqid_accession, c('qseqid_prefix', 'qseqid_acc'), sep = '_') %>%
  unite(sseqid_accession, c('sseqid_prefix', 'sseqid_acc'), sep = '_') 

df_blast <- df_blast %>%
  filter(qseqid_accession %in% accessions) %>%
  filter(sseqid_accession %in% accessions) %>%
  group_by(qseqid) %>%
  mutate(num_homologues = length(unique(sseqid_accession))) %>%
  ungroup()
  
df_cons <- df_blast %>%
  filter(num_homologues == 9)
