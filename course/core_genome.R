library(tidyverse)
library(ggthemes)

df <- read.delim("~/master/course/dataflow/04-tables/prevotella_comparison.txt", header=FALSE)
colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df <- df %>%
  select(qseqid, sseqid, pident, evalue, bitscore, qlen, length) %>%
  mutate(per_cov = (length/qlen) * 100) %>%
  filter(per_cov > 70) %>%
  filter(pident > 60)


ggplot(df, aes(x=pident)) + 
  geom_histogram(colour="black", fill="white", binwidth=1) + 
  geom_density(alpha=.2, fill="#FF6666") + 
  theme_classic()


