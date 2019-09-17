library(tidyverse)

df <- read.delim("~/master/rumen2/dataflow_test/02-blast-out/metagenome_genes_campylobacter_coli.txt", header=FALSE)
colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df <- df %>%
  mutate(per_cov = (length / qlen) * 100) %>%
  filter(per_cov > 98) %>%
  filter(pident > 99)
  
df_freq <- as.data.frame(table(df$qseqid)) %>%
  filter(Freq > 0) %>%
  arrange(desc(Freq))

hist(df_freq$Freq, breaks = 100)

hist(df_freq$Freq,
     main="sub-sample of highly conserved genes - c.coli",
     xlab="frequency - genomes",
     ylab="frequency - genes",
     col="darkmagenta",
     breaks=100
)

#

df <- read.delim("~/master/rumen2/dataflow_test/02-blast-out/metagenome_genes_listeria_monocytogenes.txt", header=FALSE)
colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df <- df %>%
  mutate(per_cov = (length / qlen) * 100) %>%
  filter(per_cov > 98) %>%
  filter(pident > 99)

df_freq <- as.data.frame(table(df$qseqid)) %>%
  filter(Freq > 0) %>%
  arrange(desc(Freq))

hist(df_freq$Freq, breaks = 100)

hist(df_freq$Freq,
     main="sub-sample of highly conserved genes - c.coli",
     xlab="frequency - genomes",
     ylab="frequency - genes",
     col="darkmagenta",
     breaks=100
)