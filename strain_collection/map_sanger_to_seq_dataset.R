library(tidyverse)

### vicki, cow

df_blast <- read.delim("~/master/strain_collection/02-blast/strains_to_neubauer.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast <- df_blast %>%
  filter(pident > 97) %>%
  select(qseqid, sseqid, pident, length)


df_count <- read.delim("~/master/strain_collection/03-tables/neubauer_et_al_epithelial.txt", skip = 1)
names(df_count)[1] <- 'sseqid'

df_meta <- read.csv("~/master/strain_collection/00-meta/neubauaer_mapping.csv")
df_meta$sample <- paste("P", df_meta$ID, sep = "")

df_classification <- read.csv("~/master/strain_collection/03-tables/bacterial_classification.csv")
df_classification$X <- NULL
names(df_classification)[1] <- c("qseqid")

df_final_neubauer <- df_count %>%
  gather(sample, count, -sseqid) %>%
  group_by(sample) %>%
  mutate(total_reads = sum(count)) %>%
  ungroup() %>%
  full_join(df_blast) %>%
  filter(count > 0) %>%
  mutate(percent_sample = (count / total_reads) * 100) %>%
  filter(qseqid != 'NA') %>%
  inner_join(df_meta) %>%
  inner_join(df_classification) %>%
  select(sseqid, sample, count, total_reads, qseqid, pident, length, percent_sample, Phase, CowName, order, family, genus)

df_final_actino <- df_final_neubauer %>%
  filter(order == "Actinomycetales")

df_final_beta <- df_final_neubauer %>%
  filter(order == "Neisseriales")

df_final_befido <- df_final_neubauer %>%
  filter(order == "Bifidobacteriales")  



### peffi, cow

df_blast <- read.delim("~/master/strain_collection/02-blast/strains_to_wetzels.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast <- df_blast %>%
  filter(pident > 97) %>%
  select(qseqid, sseqid, pident, length)


df_count <- read.delim("~/master/strain_collection/03-tables/wetzels_et_al_epithelial.txt", skip = 1)
names(df_count)[1] <- 'sseqid'

df_meta <- read.csv("~/master/strain_collection/00-meta/wetzels_epithelial.csv")
df_meta$sample <- paste("X", df_meta$ID, sep = "")

df_classification <- read.csv("~/master/strain_collection/03-tables/bacterial_classification.csv")
df_classification$X <- NULL
names(df_classification)[1] <- c("qseqid")

df_final_wetzels <- df_count %>%
  gather(sample, count, -sseqid) %>%
  group_by(sample) %>%
  mutate(total_reads = sum(count)) %>%
  ungroup() %>%
  full_join(df_blast) %>%
  filter(count > 0) %>%
  mutate(percent_sample = (count / total_reads) * 100) %>%
  filter(qseqid != 'NA') %>%
  inner_join(df_meta) %>%
  inner_join(df_classification) %>%
  select(sseqid, sample, count, total_reads, qseqid, pident, length, percent_sample, Time, Model, Run, Cow, order, family, genus)


df_final_actino <- df_final_wetzels %>%
  filter(order == "Actinomycetales")

df_final_beta <- df_final_wetzels %>%
  filter(order == "Neisseriales")

df_final_befido <- df_final_wetzels %>%
  filter(order == "Bifidobacteriales")



