library(tidyverse)

df <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_signal_differential_mapped", header=FALSE)

colnames(df) <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_select <- df %>%
  filter(length == 190) %>%
  filter(pident >= 97) %>%
  separate(qseqid, into = c("qseqid", "direction"), sep = '_')


df_select <- as.data.frame(df_select)
df_select$sseq <- as.character(df_select$sseq)
df_select$qseqid <- as.character(df_select$qseqid)

df_select_list <- list()
k <- 1

for (j in 1:nrow(df_select)) {
  
  direction <- df_select[j,2]
  newseqid <- substr(df_select[j,1], 1, 3)
  
  if (direction == "increase" ){ 
    header <- paste(">", newseqid, "_IN_" , toString(j), sep = "") 
  } else {
    header <- paste(">", newseqid, "_DE_", toString(j), sep = "") }
  
  
  df_select_list[[k]] <- header
  k <- k + 1
  
  seq <- df_select[j,14]
  
  df_select_list[[k]] <- seq
  k <- k + 1
  
  
  
}

selected_long <- as.matrix(unlist(rbind(df_select_list)))
selected_long <- gsub("\"", "", selected_long)

write.table(selected_long, "~/master/rumen/dataflow/01-nucl/lacto_signal_differential_all_seqs.fasta", row.names = FALSE, 
            col.names = FALSE, quote = FALSE)