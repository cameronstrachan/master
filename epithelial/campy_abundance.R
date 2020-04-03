library(tidyverse)


df_count <- read.delim("~/master/strain_collection/03-tables/neubauer_et_al_epithelial.txt", skip = 1)
names(df_count)[1] <- 'sseqid'

df_meta <- read.csv("~/master/strain_collection/00-meta/neubauaer_mapping.csv")
df_meta$sample <- paste("P", df_meta$ID, sep = "")

df_final_neubauer <- df_count %>%
  gather(sample, count, -sseqid) %>%
  group_by(sample) %>%
  mutate(total_reads = sum(count)) %>%
  ungroup() %>%
  filter(count > 0) %>%
  mutate(percent_sample = (count / total_reads) * 100) %>%
  inner_join(df_meta) %>%
  filter(sseqid == '6cbd388610e4c0e2359a1b9a1c0021f4')

df_plot1 <- df_final_neubauer %>%
  filter(Phase == 'Baseline')

ggplot(df_plot1, aes(x=Additive, y=percent_sample, color=Additive)) + 
  geom_boxplot() + 
  geom_jitter(shape=16, position=position_jitter(0.2))

ggplot(df_final_neubauer, aes(x=Phase, y=percent_sample, color=Phase)) + 
  geom_boxplot() + 
  geom_jitter(shape=16, position=position_jitter(0.2))

ggplot(df_final_neubauer, aes(x=CowName, y=percent_sample, color=CowName)) + 
  geom_boxplot() + 
  geom_jitter(shape=16, position=position_jitter(0.2)) + 
  theme_clean()

