library(tidyverse)
library(rRDP)
library(RColorBrewer)

## CLASSIFICATION

seq <- readDNAStringSet("~/master/uterine/dataflow/03-asv-seqs/forward-dna-sequences.fasta")
pred <- predict(rdp(), seq)
conf <- attr(pred, "confidence")

pred$asv_id <- row.names(pred)
conf <- as.data.frame(conf)
colnames(conf) <- paste(colnames(conf), "conf", sep = "_")
conf$asv_id <- row.names(conf)

df_taxa <- inner_join(pred, conf) %>%
  select(asv_id, domain, domain_conf, phylum, phylum_conf, class, class_conf, order, order_conf, family, family_conf, genus, genus_conf)

write.csv(df_taxa, '~/master/uterine/dataflow/04-exported-tables/forward-classification.csv')

## TAXA AND COUNTS

df_taxa <- read.csv('~/master/uterine/dataflow/04-exported-tables/forward-classification.csv')
df_taxa$X <- NULL

df_counts <- read.csv("~/master/uterine/dataflow/03-asv-table/forward-feature-table.txt", sep = '\t', skip = 1)
colnames(df_counts)[1] <- "asv_id"

df_counts_melt <- df_counts %>%
  gather(accession, counts, -asv_id)

df_counts_melt$accession <- as.character(df_counts_melt$accession)

## META DATA

df_dada2 <- read.csv("~/master/uterine/dataflow/00-meta/dada2_stats.csv")
df_dada2$accession <- as.character(df_dada2$accession)

df_map <- read.csv("~/master/uterine/dataflow/00-meta/knudsen_meta.csv")
df_map$accession <- as.character(df_map$accession)
df_map$sample_type <- as.character(df_map$sample_type)
df_map$time <- as.character(df_map$time)
df_map$disease_state <- as.character(df_map$disease_state)

df_meta <- inner_join(df_map, df_dada2)

## FINAL DATA FRAME

df_final <- inner_join(df_counts_melt, df_meta) %>%
  inner_join(df_taxa)

write.csv(df_final, '~/master/uterine/dataflow/04-exported-tables/df_forward_compiled.csv')  



