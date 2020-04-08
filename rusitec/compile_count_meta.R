library(tidyverse)
library(rRDP)
library(RColorBrewer)

## CLASSIFICATION

# seq <- readDNAStringSet("~/master/rusitec/dataflow/03-asv-seqs/forward-dna-sequences.fasta")
# pred <- predict(rdp(), seq)
# conf <- attr(pred, "confidence")
# 
# pred$asv_id <- row.names(pred)
# conf <- as.data.frame(conf)
# colnames(conf) <- paste(colnames(conf), "conf", sep = "_")
# conf$asv_id <- row.names(conf)
# 
# df_taxa <- inner_join(pred, conf) %>%
#   select(asv_id, domain, domain_conf, phylum, phylum_conf, class, class_conf, order, order_conf, family, family_conf, genus, genus_conf)
# 
# write.csv(df_taxa, '~/master/rusitec/dataflow/04-exported-tables/forward-classification.csv')

## TAXA AND COUNTS

df_taxa <- read.csv('~/master/rusitec/dataflow/04-exported-tables/forward-classification.csv')
df_taxa$X <- NULL

df_counts <- read.csv("~/master/rusitec/dataflow/03-asv-table/forward-feature-table.txt", sep = '\t', skip = 1)
colnames(df_counts)[1] <- "asv_id"

df_counts_melt <- df_counts %>%
  gather(sample, counts, -asv_id)

df_counts_melt$sample <- gsub("X", "", df_counts_melt$sample)
df_counts_melt$sample <- as.character(df_counts_melt$sample)

## META DATA

df_dada2 <- read.csv("~/master/rusitec/dataflow/00-meta/dada2_stats.csv")
df_dada2$sample <- as.character(df_dada2$sample)

df_vbc_map <- read.csv("~/master/rusitec/dataflow/00-meta/vbc_sample_map.csv")
df_vbc_map$run <- as.character(df_vbc_map$run)
df_vbc_map$reactor <- as.character(df_vbc_map$reactor)
df_vbc_map$sample <- as.character(df_vbc_map$sample)
df_vbc_map$time <- as.character(df_vbc_map$time)

df_tp <- read.csv("~/master/rusitec/dataflow/00-meta/meta_TP.csv")
df_tp$time <- as.character(df_tp$time)

df_t48 <- read.csv("~/master/rusitec/dataflow/00-meta/meta_T48.csv")
df_t48$run <- '48'

df_t49 <- read.csv("~/master/rusitec/dataflow/00-meta/meta_T49.csv")
df_t49$run <- '49'

df_runs <- rbind(df_t48, df_t49)
df_runs$run <- as.character(df_runs$run)
df_runs$reactor <- as.character(df_runs$reactor)

df_meta <- inner_join(df_dada2, df_vbc_map) %>%
  left_join(df_tp) %>%
  left_join(df_runs)

## FINAL DATA FRAME

df_final <- inner_join(df_counts_melt, df_meta) %>%
  inner_join(df_taxa)

write.csv(df_final, '~/master/rusitec/dataflow/04-exported-tables/df_forward_compiled.csv')  



