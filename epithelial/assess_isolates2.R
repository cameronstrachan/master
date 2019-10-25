library(tidyverse)

### all

df_blast <- read.delim("~/master/epithelial/dataflow/02-blast/sanger_epithelial_cultured_strains_to_baseline.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast <- df_blast %>%
  filter(pident >= 98) %>%
  select(qseqid, sseqid, pident, length)

colnames(df_blast)[2] <- 'asv'

df_class <- read.csv('~/master/epithelial/dataflow/04-classification/classification.csv')
df_class$X <- NULL
colnames(df_class)[1] <- 'qseqid'

df_meta <- read.csv("~/master/epithelial/dataflow/00-meta/sample_mapping.csv")
df_meta[] <- lapply(df_meta, as.character)

counts <- read.delim("~/master/epithelial/dataflow/03-asv-table/neubauer2018_wetzels2017_99.txt", header=FALSE)
counts <- counts[-1,]
counts[] <- lapply(counts, as.character)
names(counts) <- counts[1,]
counts <- counts[-1,]
counts[,2:57] <- lapply(counts[,2:57], as.numeric)
names(counts)[1] <- "asv"

df_counts <- gather(counts, ID, count, -asv) %>%
  inner_join(df_meta) %>% 
  group_by(ID) %>%
  mutate(reads= sum(count)) %>%
  ungroup() %>%
  mutate(counts_normalized = (count / reads)*100) %>%
  inner_join(df_blast) %>%
  inner_join(df_class) %>%
  filter(counts_normalized > 0) %>%
  #filter(order != 'Lactobacillales') %>%
  #filter(Type != "digesta")

# core


df_blast <- read.delim("~/master/epithelial/dataflow/02-blast/sanger_epithelial_cultured_strains_to_core.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast <- df_blast %>%
  filter(pident >= 98) %>%
  select(qseqid, sseqid, pident, length)

colnames(df_blast)[2] <- 'asv'

df_class <- read.csv('~/master/epithelial/dataflow/04-classification/classification.csv')
df_class$X <- NULL
colnames(df_class)[1] <- 'qseqid'

df_meta <- read.csv("~/master/epithelial/dataflow/00-meta/sample_mapping.csv")
df_meta[] <- lapply(df_meta, as.character)

counts <- read.delim("~/master/epithelial/dataflow/03-asv-table/neubauer2018_wetzels2017_99.txt", header=FALSE)
counts <- counts[-1,]
counts[] <- lapply(counts, as.character)
names(counts) <- counts[1,]
counts <- counts[-1,]
counts[,2:57] <- lapply(counts[,2:57], as.numeric)
names(counts)[1] <- "asv"

df_counts <- gather(counts, ID, count, -asv) %>%
  inner_join(df_meta) %>% 
  group_by(ID) %>%
  mutate(reads= sum(count)) %>%
  ungroup() %>%
  mutate(counts_normalized = (count / reads)*100) %>%
  inner_join(df_blast) %>%
  inner_join(df_class) %>%
  filter(counts_normalized > 0) %>%
  filter(order != 'Lactobacillales')
