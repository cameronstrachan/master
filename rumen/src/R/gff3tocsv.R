df_gff3 <- read.delim("~/master/rumen/dataflow/01-prot/genes/rumen_prevotella.gff3", header=FALSE, comment.char="#") %>%
  separate(V9, c("ID"), sep = ";") %>%
  select(-V2, -V3, -V6, -V8)

df_gff3$ID <- gsub("ID=", "", df_gff3$ID)

colnames(df_gff3)[1:4] <- c("contig", "start", "end", "direction")

write.csv(df_gff3, "~/master/rumen/dataflow/00-meta/rumen_prevotella.csv")