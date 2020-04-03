library(tidyverse)
library(stringi)

df <- read.delim("~/master/for_anna/tara/16s_tara_rep_seqs.txt", header=FALSE)

colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")


df_headers <- read.delim("~/master/for_anna/tara/header_16s_long.csv", header=TRUE)
df_headers$organism
df_headers$qseqid

for (i in 1:nrow(df_headers)){
  df_headers[i,"organism"] <- str_split_fixed(df_headers[i,"id"], " ", 2)[[2]]
  df_headers[i,"qseqid"] <- str_split_fixed(df_headers[i,"id"], " ", 2)[[1]]
}


df_final <- inner_join(df, df_headers)

qplot(df_final$organism, df_final$pident) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
