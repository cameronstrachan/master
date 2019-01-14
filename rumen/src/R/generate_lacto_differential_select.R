library(tidyverse)

sigtab <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_DESeq_sigtab_1000.csv")

sigtab$genus <- as.character(sigtab$genus)
sigtab$family <- as.character(sigtab$family)
sigtab$genus[is.na(sigtab$genus)] <- "None"
sigtab$family[is.na(sigtab$family)] <- "None"

sigtab <- sigtab %>%
  rename(asv_id = X) %>%
  filter(pvalue < 0.1) %>%
  filter(genus != "Lactobacillus") %>%
  filter(log2FoldChange > 3 | log2FoldChange < -3) %>%
  rowwise() %>%
  mutate(direction = ifelse(log2FoldChange > 0, "increase", "decrease")) %>%
  select(asv_id, direction, log2FoldChange) %>%
  mutate(FoldChange = 2 * log2FoldChange) %>%
  distinct() %>%
  filter(asv_id != "8accdfa41f6c21037bec2dd15596a0da") %>%
  
  filter(asv_id != "35a80099ec8e35626e6292bb8df08227") %>%
  filter(asv_id != "46ffa0bf325adaec7652afc11bcdddfe") %>%
  filter(asv_id != "dfd29bc8e5b3446c70d0f12def862834") %>%
  filter(asv_id != "584d5155a7ad9445db726adfcc1a0c2e") %>%
  filter(asv_id != "5f22ca53ac9778028d8a191e7028e5e4") 
  

write.csv(sigtab, "~/master/rumen/dataflow/00-meta/lacto_signal_differential.csv")

selected_seq_ids <- unique(sigtab$asv_id)

df_metrics <- read.csv("~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000.csv")
df_plot <- df_metrics[df_metrics$asv_id %in% selected_seq_ids,]
write.csv(df_plot, "~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-99_df_metrics_lacto_1000_df_plot.csv")
