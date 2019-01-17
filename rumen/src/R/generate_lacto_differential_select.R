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
  

write.csv(sigtab, "~/master/rumen/dataflow/00-meta/lacto_signal_differential.csv")

selected_seq_ids <- unique(sigtab$asv_id)

df_metrics <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000.csv")
df_plot <- df_metrics[df_metrics$asv_id %in% selected_seq_ids,]
write.csv(df_plot, "~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000_df_plot.csv")
