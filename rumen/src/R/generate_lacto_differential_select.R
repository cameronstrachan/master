library(tidyverse)

sigtab <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_DESeq_sigtab_1000.csv")

sigtab$genus <- as.character(sigtab$genus)
sigtab$family <- as.character(sigtab$family)
sigtab$genus[is.na(sigtab$genus)] <- "None"
sigtab$family[is.na(sigtab$family)] <- "None"

sigtab <- sigtab %>%
  rename(asv_id = X) %>%
  filter(pvalue < 0.1) %>%
  filter(family != "Lactobacillaceae") %>%
  filter(log2FoldChange > 2 | log2FoldChange < -2) %>%
  rowwise() %>%
  mutate(direction = ifelse(log2FoldChange > 0, "increase", "decrease")) %>%
  select(asv_id, direction, log2FoldChange) %>%
  mutate(FoldChange = 2 * log2FoldChange) %>%
  distinct()

selected_seq_ids <- unique(sigtab$asv_id)

df_metrics <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000.csv")
df_plot <- df_metrics[df_metrics$asv_id %in% selected_seq_ids,]


df_plot$genus <- as.character(df_plot$genus)
df_plot$family <- as.character(df_plot$family)
df_plot$genus[is.na(df_plot$genus)] <- "None"
df_plot$family[is.na(df_plot$family)] <- "None"

df_plot <- df_plot %>% 
  filter(family != "Lactobacillaceae") 

df_plot_select <- df_plot %>% 
  group_by(asv_id, lacto_signal) %>%
  top_n(3, count_norm) %>%
  ungroup() 

df_plot_select_rank <- df_plot_select %>%
  
  select(asv_id, lacto_signal, count_norm) %>%
  
  group_by(asv_id, lacto_signal) %>%
  
  summarise(value = list(count_norm)) %>%
  
  spread(lacto_signal, value) %>%
  
  group_by(asv_id) %>%
  
  mutate(mean_pos = median(unlist(pos))) %>%
  mutate(mean_neg = median(unlist(neg))) %>%
  
  ungroup() %>%
  rowwise() %>%
  
  mutate(ratio_pos = mean_pos / mean_neg) %>%
  
  mutate(ratio_neg = mean_neg / mean_pos) %>%
  
  ungroup() %>%
  
  select(asv_id, ratio_pos, ratio_neg) %>%
  
  distinct() %>%
  
  gather(direction, ratio, -asv_id)  %>%
  
  filter(ratio > 10) %>%
  
  select(-direction)

df_plot <- df_plot %>%
  inner_join(df_plot_select_rank) 

selected_seq_ids <- unique(df_plot$asv_id)

sigtab <- sigtab[sigtab$asv_id %in% selected_seq_ids,]


write.csv(df_plot, "~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000_df_plot.csv")
write.csv(sigtab, "~/master/rumen/dataflow/00-meta/lacto_signal_differential.csv")