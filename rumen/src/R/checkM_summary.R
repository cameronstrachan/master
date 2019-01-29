library(tidyverse)
library(stringi)

df <- read_csv("dataflow/02-checkmout/qa_out.log", col_names = FALSE, skip = 1)
header <- df[1,]
df <- df[-c(1, 2,1849),]

df$X1 <- gsub("  ", " ", df$X1)
df$X1 <- gsub("  ", " ", df$X1)
df$X1 <- gsub("  ", " ", df$X1)
df$X1 <- gsub("  ", " ", df$X1)
df$X1 <- gsub("  ", " ", df$X1)
df$X1 <- gsub("  ", " ", df$X1)
df$X1 <- gsub("  ", " ", df$X1)

df <- df %>%
  separate(X1, into = paste("V", seq(1,15, 1), sep = ""), sep = " ")

colnames(df) <- c("BinID", "MarkerLineage", "MarkerLineage2", "Genomes", "Markers", "MarkerSets", "0", "1", "2", "3", "4", "5+", "Completeness", "Contamination", "Heterogeneity")

df$BinID <- gsub("_rename", "", df$BinID)


df_rumen <- read.csv("dataflow/00-meta/rumen_genome_contigs.csv")
df_rumen$X <- NULL

df_rumen <- df_rumen %>%
  rowwise() %>%
  mutate(genome = stri_reverse(stri_split_fixed(stri_reverse(X0),"_",n = 2)[[1]][2])) %>%
  select(-X0) %>%
  distinct()
  
df_rumen$genome <- gsub(">", "", df_rumen$genome)
df_rumen$source <- "rumen"
colnames(df_rumen)[1] <- "BinID"

df <- left_join(df, df_rumen) 

write.csv(df, "dataflow/00-meta/checkM_summary_clean.csv")

df_prevotella <- df %>%
  filter(MarkerLineage == "g__Prevotella")

write.csv(df_prevotella, "dataflow/00-meta/checkM_summary_clean_prevotella.csv")
