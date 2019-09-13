library(tidyverse)

# calculate core asvs

meta <- read.csv("~/master/epithelial/dataflow/00-meta/sample_mapping.csv")
meta[] <- lapply(meta, as.character)

counts <- read.delim("~/master/epithelial/dataflow/03-asv-table/neubauer2018_wetzels2017_99.txt", header=FALSE)
counts <- counts[-1,]
counts[] <- lapply(counts, as.character)
names(counts) <- counts[1,]
counts <- counts[-1,]
counts[,2:57] <- lapply(counts[,2:57], as.numeric)
names(counts)[1] <- "asv"

df <- gather(counts, ID, count, -asv) %>%
  inner_join(meta) %>% 
  group_by(ID) %>%
  mutate(reads= sum(count)) %>%
  ungroup() %>%
  mutate(counts_normalized = (count / reads)*100)
  

df_differential <- df %>%
  filter(Study == 'Neubauer2018') %>%
  group_by(asv, Type) %>%
  mutate(mean_counts_normalized  = mean(counts_normalized)) %>%
  ungroup() %>%
  select(asv, Type, mean_counts_normalized) %>%
  distinct() %>%
  spread(Type, mean_counts_normalized) %>%
  mutate(fold_change = epithelial / digesta) %>%
  mutate(fold_change_cat = if_else(is.nan(fold_change), 0,
                                   if_else(fold_change == Inf, 500, fold_change))) %>%
  filter(fold_change_cat > 0) %>%
  filter(epithelial > 0.1) %>%
  select(asv, fold_change_cat)

df_prevalence <- df %>%
  inner_join(df_differential) %>%
  filter(Type == 'epithelial') %>%
  mutate(detected = if_else(count > 0, 1, 0)) %>%
  group_by(asv) %>%
  mutate(per_samples_detected = sum(detected) / 48) %>%
  mutate(mean_counts_normalized = mean(counts_normalized)) %>%
  ungroup() %>%
  select(asv, mean_counts_normalized,  per_samples_detected, fold_change_cat) %>%
  distinct() %>%
  filter(fold_change_cat > 5)

# classify  

library(rRDP)

seq <- readDNAStringSet("~/master/epithelial/dataflow/03-asv-seqs/neubauer2018_wetzels201_99.fasta")
pred <- predict(rdp(), seq)
conf <- attr(pred, "confidence")

pred$asv <- row.names(pred)
conf <- as.data.frame(conf)
colnames(conf) <- paste(colnames(conf), "conf", sep = "_")
conf$asv <- row.names(conf)

df_taxa <- inner_join(pred, conf) %>%
  select(asv, domain, domain_conf, phylum, phylum_conf, class, class_conf, order, order_conf, family, family_conf, genus, genus_conf)

write.csv(df_taxa, "~/master/epithelial/dataflow/00-meta/neubauer2018_wetzels201_99_rdp.csv")


# combine and define core

df_final <- inner_join(df_prevalence, df_taxa) 

total_percent <- sum(df_final$mean_counts_normalized)

df_final <- df_final %>%
  mutate(per_core_mean_counts_normalized = (mean_counts_normalized / total_percent)*100) %>%
  group_by(phylum) %>%
  mutate(phylm_per_core_mean_counts_normalized = sum(per_core_mean_counts_normalized)) %>%
  ungroup()

write.csv(df_final, "~/master/epithelial/dataflow/00-meta/core_microbiome.csv")

df_seqs <- df_final %>%
  select(asv) %>%
  distinct()

write.csv(df_seqs, "~/master/epithelial/dataflow/00-meta/core_microbiome_seqs.csv")
