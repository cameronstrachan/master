df <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_prevo_mapped", header=FALSE)

colnames(df) <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_select <- df %>%
  filter(length > 130) %>%
  filter(pident > 96) %>%
  rowwise() %>%
  mutate(seq_num = stri_reverse(stri_split_fixed(stri_reverse(sseqid),"_",n = 2)[[1]][1])) %>%
  mutate(genome = stri_reverse(stri_split_fixed(stri_reverse(sseqid),"_",n = 2)[[1]][2])) 


df_select <- as.data.frame(df_select)
df_select$sseq <- as.character(df_select$sseq)

df_select_list <- list()
k <- 1

for (j in 1:nrow(df_select)) {
  
  seq_id <- df_select[j,2]
  header <- paste(">", seq_id, sep = "")

  
  df_select_list[[k]] <- header
  k <- k + 1
  
  seq <- df_select[j,13]
  
  df_select_list[[k]] <- seq
  k <- k + 1
  
  
  
}


selected_long <- as.matrix(unlist(rbind(df_select_list)))
selected_long <- gsub("\"", "", selected_long)

write.table(selected_long, "~/master/rumen/dataflow/01-nucl/lacto_prevo_genomes_blast.fasta", row.names = FALSE, 
            col.names = FALSE, quote = FALSE)
