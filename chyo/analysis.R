library(tidyverse)

br = seq(0,1610000, by=500)

ranges = paste(head(br,-1), br[-1], sep=" - ")

files <- list.files(path = '~/master/chyo/blast_output', pattern = "\\.txt$")
file_samples <- gsub(".sorted.mapped.txt", "", files)

df_list_freq <- list()
df_list_reads <- list()
i <- 1
for (x in 1:length(files)) {
  
  df <- read.delim(paste('~/master/chyo/blast_output', files[x], sep = '/'), header=FALSE)
  colnames(df)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")
  
  df_trim <- df %>%
    mutate(per_aln = (length / qlen)*100) %>%
    filter(per_aln > 97) %>%
    filter(pident > 90) %>%
    mutate(center = round(if_else(sstart < send, (((send - sstart)/2) + sstart), (((sstart - send)/2) + send))))
  
  df_trim$sample <- file_samples[x]
  
  freq   = hist(df_trim$center, breaks=br, include.lowest=TRUE, plot=FALSE)
  df_freq <- data.frame(range = ranges, frequency = freq$counts)
  
  colnames(df_freq)[2] <- file_samples[x]
  
  df_reads <- df_trim %>%
    mutate(observation = 1:n()) %>%
    unite(header, c("observation", "sample"), sep = "_") %>%
    select(observation, sample, sseq)
  
  
  df_list_freq[[i]] <- df_freq
  df_list_reads[[i]] <- df_reads
  i <- i + 1

}

df_compiled_reads <- bind_rows(df_list_reads)
df_compiled_freq <- Reduce(function(...) merge(..., by='range', all.x=TRUE), df_list_freq)

df_meta <- read.csv("~/master/chyo/sample_mapping.csv")

df_compiled_freq <- df_compiled_freq %>% 
  mutate(observation = 1:n()) %>%
  gather(sample, count, -range, -observation) %>%
  left_join(df_meta) 
  
  
df_plot <-  df_compiled_freq %>%
  group_by(range, observation, treatment) %>%
  mutate(med_count = median(count)) %>%
  ungroup() %>%
  filter(med_count > 1)

ggplot(df_plot, aes(x=observation, y=med_count, color=treatment, fill=treatment)) +
  geom_point()

df_selected <- df_compiled_freq %>%
  group_by(range, observation, treatment) %>%
  summarise(counts = list(count)) %>%
  ungroup() %>%
  spread(treatment, counts) %>%
  rowwise() %>%
  mutate(diff_SARA = median(unlist(SARA)) - median(unlist(baseline))) %>%
  ungroup() %>%
  filter(diff_SARA > 0) %>%
  arrange(observation)

df_selected$cluster <- cumsum(c(1, abs(df_selected$observation[-length(df_selected$observation)] - df_selected$observation[-1]) > 1))

df_selected <- df_selected %>%
  group_by(cluster) %>%
  mutate(n_cluster = length(unique(observation))) %>%
  mutate(median_diff_cluster = median(diff_SARA)) %>%
  ungroup() %>%
  filter(n_cluster > 1)
