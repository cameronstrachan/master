library(tidyverse)

# compile blast results
df_list <- list()
files <- list.files("dataflow/03-blastout/", pattern = ".txt")
i <- 1

for (file in files){
  df <- read.delim(paste("dataflow/03-blastout/", file, sep = ""), header = FALSE)
  df$file <- gsub(".txt", "", file)
  df_list[[i]] <- df
  i <- i + 1
}

compiled_blast_hits <- bind_rows(df_list)
colnames(compiled_blast_hits)[1:13] <- c("qseqid", "sseqid", "blast_pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

compiled_blast_hits <- compiled_blast_hits %>%
  mutate(blast_per_aln = (length / qlen) *100) %>%
  select(qseqid, sseqid, blast_pident, blast_per_aln, file) %>%
  separate(file, into = c("genome", "category"), sep = ":")

colnames(compiled_blast_hits)[1:2] <- c("gene_id", "characterized_protein")

# compile hmm results
files <- list.files("dataflow/03-hmmout/", pattern = ".txt")

df_list <-lapply(files,function(file){
  x <- try(read.delim(paste("dataflow/03-hmmout/", file, sep = ""), header = FALSE, comment.char = "#"))
  if(inherits(x, "try-error"))
    return(NULL)
  else
    df$file <- gsub(".txt", "", file)
  return(x)
})

compiled_hmm_hits <- bind_rows(df_list) %>%
  separate(V1, into = c("hmm_domain", "hmm_pfam", "gene_id", "rm", "hmm_evalue"), sep = "\\s+") %>%
  select(-rm)

# compile genome location from prodigal headers
compiled_headers <- read.csv("dataflow/00-meta/selected_prot_headers.csv")

compiled_headers <- compiled_headers %>%
  select(-X, -index) %>%
  separate(X0, into = c("rm", "start", "stop", "direction"), sep = " # ") %>%
  select(-rm, -category) %>%
  distinct()

# compile everything and save
compiled <- full_join(compiled_headers, compiled_blast_hits) %>%
  full_join(compiled_hmm_hits) %>%
  select(genome, gene_id, start, stop, direction, characterized_protein, blast_pident, blast_per_aln, hmm_domain, hmm_evalue) %>%
  distinct()

write.csv(compiled, 'dataflow/04-analysis-tables/compiled_lactate_annotations.csv', row.names = FALSE)

