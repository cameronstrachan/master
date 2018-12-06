df <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_prevo_100_mapped", header=FALSE)

colnames(df) <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_select <- df %>%
  filter(length > 320) %>%
  filter(pident > 97)


df_select <- as.data.frame(df_select)
df_select$sseq <- as.character(df_select$sseq)
df_select$qseqid <- as.character(df_select$qseqid)

df_select_list <- list()
k <- 1

for (j in 1:nrow(df_select)) {
  
  seq_id <- df_select[j,1]
  
  if (seq_id == "cebd44fd058a519d1dc298117fae3289_negative_correlation" ){ 
      header <- paste(">", 'CEB_N.', toString(j), sep = "") 
  } else if (seq_id == "c485fc827ccec5c2eaae3253455939ba_negative_correlation") { 
    header <- paste(">", 'C48_N.', toString(j), sep = "") 
    }
   else {
      header <- paste(">", '8CB_P.', toString(j), sep = "") }

  
  df_select_list[[k]] <- header
  k <- k + 1
  
  seq <- df_select[j,13]
  
  df_select_list[[k]] <- seq
  k <- k + 1
  
  
  
}


selected_long <- as.matrix(unlist(rbind(df_select_list)))
selected_long <- gsub("\"", "", selected_long)

write.table(selected_long, "~/master/rumen/dataflow/01-nucl/lacto_prevo_100.fasta", row.names = FALSE, 
            col.names = FALSE, quote = FALSE)