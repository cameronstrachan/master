library(tidyverse)
library(stringi)
library(reshape2)
library(readr)
library(ggthemes)

files <- list.files('~/master/anna/dataflow/02-blast/')
blastdir <- '~/master/anna/dataflow/02-blast/'

dflist <- list()

i <- 1
for (file in files){
  df <- read.table(paste(blastdir, file, sep = ''))
  df$file <- file
  df$V1 <- as.character(df$V1)
  df$V2 <- as.character(df$V2)
  dflist[[i]] <- df
  i <- i+1
}

df_compiled <- bind_rows(dflist)
colnames(df_compiled)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_compiled$file <- gsub("\\.txt", "", df_compiled$file)

df_compiled <- df_compiled %>%
  separate(file, into = c("file1", "file2"), sep = "\\.") %>%
  mutate(piali = (length / qlen) * 100) %>%
  filter(piali > 40) %>%
  filter(pident > 30)


df_compiled$sseq <- NULL

df_forward <- df_compiled %>%
  select(qseqid, sseqid,file1, file2, pident) %>%
  rename(forward_pi = pident) %>%
  distinct()

df_reverse <- df_compiled %>%
  select(qseqid, sseqid, file1, file2, pident) %>%
  rename(reverse_pi = pident) %>%
  distinct()

colnames(df_reverse)[1:4] <- c("sseqid", "qseqid", "file2", "file1")

df_rbh <- inner_join(df_forward, df_reverse) %>%
  mutate(mean_pi = (forward_pi + reverse_pi)/2) %>%
  select(-forward_pi, -reverse_pi) %>%
  distinct() %>%
  rowwise() %>%
  mutate(samefile = ifelse(file1 == file2, "yes", "no")) %>%
  filter(samefile != "yes") %>%
  select(-samefile) 

df_rbh$sseqid[is.na(df_rbh$sseqid)] <- "None"
df_rbh$file1[is.na(df_rbh$file1)] <- "None"
df_rbh$file2[is.na(df_rbh$file2)] <- "None"
df_rbh$mean_pi[is.na(df_rbh$mean_pi)] <- 0.0

df_rbh$qseqid <- gsub("n_", "", df_rbh$qseqid)
df_rbh$sseqid <- gsub("n_", "", df_rbh$sseqid)

df_plot <- df_rbh %>%
  select(-file1, -file2) %>%
  separate(qseqid, into = c("genome1", "contig1", "gene1"), sep = "_", remove = FALSE) %>%
  separate(sseqid, into = c("genome2", "contig2", "gene2"), sep = "_", remove = FALSE) 

df_plot$gene1 <- as.numeric(df_plot$gene1)  
df_plot$gene2 <- as.numeric(df_plot$gene2)  

df_plot_stinki <- df_plot %>%
  filter(genome1 == "stinkeri") %>%
  arrange(gene1)

df_plot_noah <- df_plot %>%
  filter(genome1 == "noahi") %>%
  arrange(gene1)

### NOAHHHH

#xbreaks <- df_plot_noah$gene1[seq(1, length(df_plot_noah$gene1), 100)]

plot_noah <- ggplot(df_plot_noah, aes(x=gene1)) +
  
  theme_few() +
  
  geom_point(aes(y = mean_pi, colour = genome2), stat = "identity", size = 2) +
  
  theme(plot.title = element_text(size = 25), 
        axis.text.x = element_text(angle = 90, hjust = 1, size = 12),  
        axis.text.y = element_text(size = 20), 
        axis.title.x = element_text(size = 20), 
        axis.title.y = element_text(size = 20)) + 
  
  ylab("Percent identity (%)") + 
  
  ylim(25,100) +
  
  #theme(legend.position="none") +
  
  theme(legend.text=element_text(size=20)) + 
  theme(legend.title=element_text(size=20)) #+
  #scale_x_discrete("Ordered genes",  breaks = xbreaks)

plot_noah

#### STINKIIII

#xbreaks <- df_plot_stinki$gene1[seq(1, length(df_plot_stinki$gene1), 100)]

plot_stinki <- ggplot(df_plot_stinki, aes(x=gene1)) +
  
  theme_few() +
  
  geom_point(aes(y = mean_pi, colour = genome2), stat = "identity", size = 2) +
  
  theme(plot.title = element_text(size = 25), 
        axis.text.x = element_text(angle = 90, hjust = 1, size = 12),  
        axis.text.y = element_text(size = 20), 
        axis.title.x = element_text(size = 20), 
        axis.title.y = element_text(size = 20)) + 
  
  ylab("Percent identity (%)") + 
  
  ylim(25,100) +
  
  #theme(legend.position="none") +
  
  theme(legend.text=element_text(size=20)) + 
  theme(legend.title=element_text(size=20)) #+
  #scale_x_discrete("Ordered genes",  breaks = xbreaks)

plot_stinki
