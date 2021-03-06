library(tidyverse)
library(stringi)

df1 <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_signal_differential_all_seqs_prevotella_genomes_mapped", header=FALSE)
df1$database <- "Prevotella"

df2 <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_signal_differential_all_seqs_rumen_genomes_mapped", header=FALSE)
df2$database <- "Rumen"


df <- bind_rows(df1, df2)

colnames(df) <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq", "database")

df$length <- as.numeric(df$length)
df$pident <- as.numeric(df$pident)
df$bitscore <- as.numeric(df$bitscore)

df_select <- df %>%
  filter(length == 190) %>%
  filter(pident >= 95) %>%
  rowwise() %>%
  mutate(seq_num = stri_reverse(stri_split_fixed(stri_reverse(sseqid),"_",n = 2)[[1]][1])) %>%
  mutate(genome = stri_reverse(stri_split_fixed(stri_reverse(sseqid),"_",n = 2)[[1]][2])) 


df_select$genome <- gsub("_genomic", "", df_select$genome)
df_select$genome <- gsub("-submission.assembly", "", df_select$genome)
df_select$genome <- gsub("_annotated_assembly", "", df_select$genome)

df_select <- as.data.frame(df_select)
df_select$sseq <- as.character(df_select$sseq)

df_select_list <- list()
k <- 1
already_done <- c()

for (j in 1:nrow(df_select)) {
  
  database <- df_select[j,14]
  genome <- df_select[j,16]
  header <- paste(">", database, "_", genome,  "_", toString(j), sep = "")
  
  if ( !(genome %in% already_done) ){
  
  df_select_list[[k]] <- header
  k <- k + 1
  
  seq <- df_select[j,13]
  
  df_select_list[[k]] <- seq
  k <- k + 1
  
  already_done <- c(already_done, genome)
  
  }

}


selected_long <- as.matrix(unlist(rbind(df_select_list)))
selected_long <- gsub("\"", "", selected_long)

write.table(selected_long, "~/master/rumen/dataflow/01-nucl/lacto_signal_differential_all_seqs_genomes.fasta", row.names = FALSE, col.names = FALSE, quote = FALSE)
