library(tidyverse)

#
df_headers <- read.csv("~/master/rumen2/dataflow/03-analysis/stewart2019_mags_genes_300_cp_mapped_headers.csv")
df_headers$X <- NULL

colnames(df_headers)[1] <- c('qseqid')

df_headers <- df_headers %>%
  select(qseqid, full_header) %>%
  separate(full_header, into = c("rm", "start", "stop", "direction"), sep = " # ") %>%
  select(-rm)
#

#files <- c("stewart2019_mags_genes_300_cp_acinetobacter_baumannii.txt", "stewart2019_mags_genes_300_cp_neisseria_gonorrhoeae.txt", "stewart2019_mags_genes_300_cp_campylobacter_coli.txt", "stewart2019_mags_genes_300_cp_pathogen_mapped_card.txt", "stewart2019_mags_genes_300_cp_campylobacter_jejuni.txt", "stewart2019_mags_genes_300_cp_pseudomonas_aeruginosa.txt", "stewart2019_mags_genes_300_cp_clostridioides_difficile.txt", "stewart2019_mags_genes_300_cp_staphylococcus_aureus.txt", "stewart2019_mags_genes_300_cp_listeria_monocytogenes.txt", "stewart2019_mags_genes_300_cp_streptococcus_pneumoniae.txt")
files <- c('stewart2019_mags_genes_300_dave_clostridioides_difficile_dave.txt')

list_files <- list()
i <- 1

for (file in files){
file_in <- paste("~/master/rumen2/dataflow/02-blast-out/", file, sep = '')
df <- read.delim(file_in, header=FALSE)
colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df <- df %>%
  mutate(per_cov = (length / qlen) * 100) %>%
  filter(per_cov > 98) %>%
  filter(pident > 99) %>%
  select(qseqid, sseqid, pident, sstart, send) %>%
  inner_join(df_headers)
  paste("~/master/rumen2/dataflow/03-analysis/start_stop_", file, sep = '')
  
  write.csv(df, paste("~/master/rumen2/dataflow/03-analysis/start_stop_", file, sep = ''))
i <- i + 1
}
