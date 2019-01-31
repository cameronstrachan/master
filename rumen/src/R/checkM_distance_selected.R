library(readr)
library(tidyverse)
library(ape)
library(stringr)
library(distory)
library(adephylo)

checkM_summary_clean_prevotella <- read_csv("dataflow/00-meta/checkM_summary_clean_prevotella.csv")

checkM_summary_clean_prevotella_rumen <- checkM_summary_clean_prevotella %>%
  filter(source == "rumen") %>%
  rowwise() %>%
  mutate(genome = paste(BinID, "rename", sep = "_"))


genomes <- unique(checkM_summary_clean_prevotella_rumen$genome)


tree <- read.tree("dataflow/03-trees/concatenated.tre")


df_dist <- as.matrix(distTips(tree))

df_dist_sub <- df_dist[row.names(df_dist) %in% genomes, colnames(df_dist) %in% genomes]

write.csv(df_dist_sub, "dataflow/04-analysis-tables/rumen_prevotella_checkMtree_distance.csv")