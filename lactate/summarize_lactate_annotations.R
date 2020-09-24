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

# compile everything and trim for blast hits that align with less than half the protein
characterized_proteins_map <- read.csv("dataflow/00-meta/characterized_proteins.csv") %>%
  select(characterized_protein, annotation, gene)

compiled <- full_join(compiled_headers, compiled_blast_hits) %>%
  full_join(compiled_hmm_hits) %>%
  full_join(characterized_proteins_map ) %>%
  filter(blast_per_aln > 50) %>%
  select(genome, gene_id, gene, annotation, start, stop, direction, blast_pident, blast_per_aln, hmm_domain, hmm_evalue) %>%
  distinct()

# L to D correction based on 2 domains
compiled$annotation <- as.character(compiled$annotation )

compiled_corrected <- compiled %>%
  group_by(genome, gene_id) %>%
  mutate(annotation = if_else("2-Hacid_dh_C" %in% hmm_domain | "2-Hacid_dh" %in% hmm_domain, "D-Lactate production", unique(annotation))) %>%
  ungroup()
  
# check that expected domains are present and catogorize producers by having L-Lactate production genes and L-lactate utilizers by having a permase and a utilization gene
expected_domains <- read.csv("dataflow/00-meta/characterized_proteins_expected_domains.csv")

complete_gene_count_summary <- compiled_corrected %>%
  inner_join(expected_domains) %>%
  group_by(genome, gene_id, gene) %>%
  mutate(domain_summary = if_else(all(expected_domains %in% hmm_domain), "complete", "incomplete")) %>%
  ungroup() %>%
  filter(domain_summary == "complete") %>%
  select(genome, gene_id, annotation) %>%
  distinct() %>%
  group_by(genome, annotation) %>%
  mutate(num_genes = length(unique(gene_id))) %>%
  ungroup() %>%
  group_by(genome) %>%
  mutate(lactate_utilizer = if_else(all(c("L-Lactate permease", "L-Lactate utilization") %in% annotation), "yes", "no")) %>%
  mutate(lactate_producer = if_else("L-Lactate production" %in% annotation, "yes", "no")) %>%
  ungroup() %>%
  select(genome, annotation, num_genes, lactate_utilizer, lactate_producer) %>%
  filter(annotation != "D-Lactate production") %>%
  distinct()

write.csv(complete_gene_count_summary, 'dataflow/04-analysis-tables/lactate_metabolism_classification.csv')

