library(tidyverse)
library(stringi)
library(reshape2)
library(readr)

checkM_summary_clean_prevotella <- read_csv("~/master/rumen/dataflow/00-meta/checkM_summary_clean_prevotella.csv")
seshadri2018_prevotella <- read_csv("~/master/rumen/dataflow/00-meta/seshadri2018_prevotella.csv")

checkM_summary_clean_prevotella_rumen <- checkM_summary_clean_prevotella %>%
  filter(source == "rumen")



blastdir <- 'dataflow/02-blast/'

genomes1 <- unique(checkM_summary_clean_prevotella_rumen$BinID)
genomes2 <- unique(seshadri2018_prevotella$file)

genomes <- unique(c(genomes1, genomes2))

files <- c()

for (genome1 in genomes){
  genome1r <- paste(genome1, "rename", sep = "_")
  for (genome2 in genomes){
    genome2r <- paste(genome2, "rename", sep = "_")
    file <- paste(genome1r, genome2r, "txt", sep = ".")
    files <- c(files, file)
  }
}

dflist <- list()

i <- 1
for (file in files){
  df <- read.table(paste(blastdir, file, sep = ''))
  df$file <- file
  df$V1 <- as.character(df$V1)
  df$V2 <- as.character(df$V2)
  dflist[[i]] <- df
  i <- i+1
}

df_compiled <- bind_rows(dflist)
colnames(df_compiled)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_compiled$file <- gsub("submission.assembly", "", df_compiled$file)
df_compiled$file <- gsub("final.assembly", "", df_compiled$file)
df_compiled$file <- gsub(".assembly", "", df_compiled$file)
df_compiled$file <- gsub("\\.1", "1", df_compiled$file)
df_compiled$file <- gsub("\\.0", "0", df_compiled$file)
df_compiled$file <- gsub("_rename", "", df_compiled$file)
df_compiled$file <- gsub("_genomic", "", df_compiled$file)
df_compiled$file <- gsub("-", "", df_compiled$file)
df_compiled$file <- gsub("_IMG-taxon_2693429877_annotated", "", df_compiled$file)
df_compiled$file <- gsub("\\.txt", "", df_compiled$file)

df_compiled <- df_compiled %>%
  separate(file, into = c("file1", "file2"), sep = "\\.") %>%
  filter(length > 100)

df_compiled$sseq <- NULL

df_forward <- df_compiled %>%
  select(qseqid, sseqid,file1, file2, pident) %>%
  rename(forward_pi = pident) %>%
  distinct()

df_reverse <- df_compiled %>%
  select(qseqid, sseqid, file1, file2, pident) %>%
  rename(reverse_pi = pident) %>%
  distinct()

colnames(df_reverse)[1:4] <- c("sseqid", "qseqid", "file2", "file1")

df_rbh <- inner_join(df_forward, df_reverse) %>%
  mutate(mean_pi = (forward_pi + reverse_pi)/2) %>%
  select(-forward_pi, -reverse_pi) %>%
  distinct() %>%
  rowwise() %>%
  mutate(samefile = ifelse(file1 == file2, "yes", "no")) %>%
  filter(samefile != "yes") %>%
  select(-samefile) #%>%
  #filter(mean_pi > 40)

df_rbh$sseqid[is.na(df_rbh$sseqid)] <- "None"
df_rbh$file1[is.na(df_rbh$file1)] <- "None"
df_rbh$file2[is.na(df_rbh$file2)] <- "None"
df_rbh$mean_pi[is.na(df_rbh$mean_pi)] <- 0.0

df_pi_shared <- df_rbh %>%
  select(file1, file2, mean_pi) %>%
  group_by(file1, file2) %>%
  mutate(mean_mean_pi = mean(mean_pi)) %>%
  ungroup() %>%
  select(-mean_pi) %>%
  distinct()

write.csv(df_rbh, "dataflow/04-analysis-tables/selected_genomes_rbh.csv")
write.csv(df_pi_shared, "dataflow/04-analysis-tables/selected_genomes_sharedPI.csv")