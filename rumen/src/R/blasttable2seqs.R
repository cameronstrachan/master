<<<<<<< HEAD
df <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_prevo_mapped", header=FALSE)

colnames(df) <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_select <- df %>%
  filter(length > 130) %>%
  filter(pident > 96) %>%
=======
df1 <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_prevo_100_prevo_genomes_mapped", header=FALSE)
df1$database <- "Prevotella"

df2 <- read.delim("~/master/rumen/dataflow/03-blast-tables/lacto_prevo_100_rumen_genomes_mapped", header=FALSE)
df2$database <- "Rumen"


df <- bind_rows(df1, df2)

colnames(df) <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq", "database")

df$length <- as.numeric(df$length)
df$pident <- as.numeric(df$pident)
df$bitscore <- as.numeric(df$bitscore)

df_select <- df %>%
  filter(length > 280) %>%
  filter(pident > 93) %>%
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4
  rowwise() %>%
  mutate(seq_num = stri_reverse(stri_split_fixed(stri_reverse(sseqid),"_",n = 2)[[1]][1])) %>%
  mutate(genome = stri_reverse(stri_split_fixed(stri_reverse(sseqid),"_",n = 2)[[1]][2])) 

<<<<<<< HEAD
=======
df_select$genome <- gsub("_genomic", "", df_select$genome)
df_select$genome <- gsub("-submission.assembly", "", df_select$genome)
df_select$genome <- gsub("_annotated_assembly", "", df_select$genome)




>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

df_select <- as.data.frame(df_select)
df_select$sseq <- as.character(df_select$sseq)

df_select_list <- list()
k <- 1

for (j in 1:nrow(df_select)) {
  
<<<<<<< HEAD
  seq_id <- df_select[j,2]
  header <- paste(">", seq_id, sep = "")
=======
  database <- df_select[j,14]
  genome <- df_select[j,16]
  header <- paste(">", database, "_", genome,  sep = "")
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4

  
  df_select_list[[k]] <- header
  k <- k + 1
  
  seq <- df_select[j,13]
  
  df_select_list[[k]] <- seq
  k <- k + 1
  
  
  
}


selected_long <- as.matrix(unlist(rbind(df_select_list)))
selected_long <- gsub("\"", "", selected_long)

<<<<<<< HEAD
write.table(selected_long, "~/master/rumen/dataflow/01-nucl/lacto_prevo_genomes_blast.fasta", row.names = FALSE, 
=======
write.table(selected_long, "~/master/rumen/dataflow/01-nucl/lacto_prevo_100_genomes_blast.fasta", row.names = FALSE, 
>>>>>>> bc63259588b9b18c1f659eccbc5b966d470663f4
            col.names = FALSE, quote = FALSE)
