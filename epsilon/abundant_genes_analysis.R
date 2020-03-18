library(tidyverse)

df <- read.csv("~/master/epsilon/dataflow/04-analysis-tables/mapped_genes.csv")

df <- df %>%
  filter(file == "11L2_ACAGTG.1_10677_0009_idba_bin.216.txt" | file == "11L2_ACAGTG.1_10677_0014_idba_bin.49.txt") %>%
  filter(id != "__alignment_not_unique") %>%
  arrange(desc(count)) %>%
  select(id, count, total, file) 


df_gff3_49 <- read.delim("~/master/epsilon/dataflow/01-gff3/10677_0014_idba_bin.49.gff3", header=FALSE, comment.char="#") %>%
  select(V1, V4, V5, V7, V9) %>%
  separate(V9, into = c("id", "rm"), sep = ";") %>%
  select(-rm)

df_gff3_49$id <- gsub("ID=", "", df_gff3_49$id)
colnames(df_gff3_49)[1:4] <- c("contig", "start", "stop", "dir")
df_gff3_49$file <- "11L2_ACAGTG.1_10677_0014_idba_bin.49.txt"

df_gff3_216 <- read.delim("~/master/epsilon/dataflow/01-gff3/10677_0009_idba_bin.216.gff3", header=FALSE, comment.char="#") %>%
  select(V1, V4, V5, V7, V9) %>%
  separate(V9, into = c("id", "rm"), sep = ";") %>%
  select(-rm)

df_gff3_216$id <- gsub("ID=", "", df_gff3_216$id)
colnames(df_gff3_216)[1:4] <- c("contig", "start", "stop", "dir")
df_gff3_216$file <- "11L2_ACAGTG.1_10677_0009_idba_bin.216.txt"

df_gff3 <- bind_rows(df_gff3_49, df_gff3_216) %>%
  inner_join(df) %>%
  group_by(contig, file) %>%
  mutate(contig_total = sum(count)) %>%
  ungroup()
