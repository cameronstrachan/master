library(tidyverse)

files <- list.files(path = '~/master/chyo/blast_output/concensus/', pattern = "\\.txt$")
file_samples <- gsub(".sorted.mapped.txt", "", files)

df_list_counts <- list()
i <- 1
for (x in 1:length(files)) {
  
  df <- read.delim(paste('~/master/chyo/blast_output/concensus/', files[x], sep = '/'), header=FALSE)
  colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")
  
  df_count <- df %>%
    mutate(per_aln = (length / qlen)*100) %>%
    filter(per_aln > 97) %>%
    filter(pident > 90) %>%
    mutate(center = round(if_else(sstart < send, (((send - sstart)/2) + sstart), (((sstart - send)/2) + send))))
  
  df_count$sseqid <- gsub("cyo_transcripome_concensus_genome_", "", df_count$sseqid)
  df_count$sample <- file_samples[x]
  
  df_list_counts[[i]] <- df_count
  i <- i + 1
  
}

df_meta <- read.csv("~/master/chyo/expressed/annotation_of_interest.csv")
df_meta$gene_num <- as.character(df_meta$gene_num)

df_compiled_counts <- bind_rows(df_list_counts) %>%
  
  group_by(sseqid) %>%
  mutate(count = length(unique(qseqid))) %>%
  ungroup() %>%
  
  select(sseqid, count) %>%
  
  distinct() %>%
  
  separate(sseqid, into = c("gene_num", "start", "stop", "dir"), sep = "_") %>%
  
  left_join(df_meta)
  


