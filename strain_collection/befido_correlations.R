library(tidyverse)

### vicki, cow

df_blast <- read.delim("~/master/strain_collection/02-blast/strains_to_neubauer.txt", header=FALSE)
colnames(df_blast)[1:13] <- c("qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq")

df_blast <- df_blast %>%
  filter(pident > 95) %>%
  select(qseqid, sseqid, pident, length)


df_count <- read.delim("~/master/strain_collection/03-tables/neubauer_et_al_epithelial.txt", skip = 1)
names(df_count)[1] <- 'sseqid'

df_meta <- read.csv("~/master/strain_collection/00-meta/neubauaer_mapping.csv")
df_meta$sample <- paste("P", df_meta$ID, sep = "")

df_classification <- read.csv("~/master/strain_collection/03-tables/bacterial_classification.csv")
df_classification$X <- NULL
names(df_classification)[1] <- c("qseqid")

df_final_neubauer <- df_count %>%
  gather(sample, count, -sseqid) %>%
  group_by(sample) %>%
  mutate(total_reads = sum(count)) %>%
  ungroup() %>%
  full_join(df_blast) %>%
  #filter(count > 0) %>%
  mutate(percent_sample = (count / total_reads) * 100) %>%
  #mutate(percent_sample = count) %>%
  filter(total_reads > 4000) %>%
  filter(qseqid != 'NA') %>%
  inner_join(df_meta) %>%
  inner_join(df_classification) %>%
  select(sseqid, sample, count, total_reads, qseqid, pident, length, percent_sample, Additive, Phase, Run, CowName, order, family, genus)

df_final_actino <- df_final_neubauer %>%
  filter(order == "Actinomycetales")

df_final_beta <- df_final_neubauer %>%
  filter(order == "Neisseriales")

df_final_befido <- df_final_neubauer %>%
  filter(order == "Bifidobacteriales") 

df_final_befido$Run <- gsub("-", "", df_final_befido$Run)

df_neub_meta <- read.csv("~/master/strain_collection/00-meta/neubauer_meta.csv")
df_neub_meta$Phase <- gsub("SARA1", "SARA_I", df_neub_meta$Phase)
df_neub_meta$Phase <- gsub("SARA2", "SARA_II", df_neub_meta$Phase)
names(df_neub_meta)[3] <- "CowName"
df_neub_meta$CowName <- gsub("Bergi", "Bergrose", df_neub_meta$CowName)
df_neub_meta$CowName <- gsub("Nevada", "Newada", df_neub_meta$CowName)

df_cor <- left_join(df_final_befido, df_neub_meta) %>%
  group_by(sample) %>%
  mutate(percent_sample = max(percent_sample)) %>%
  mutate(sample_detected = if_else(percent_sample > 0.1, 1, 0)) %>%
  ungroup() %>%
  select(-sseqid, -sample, -count, -total_reads, -qseqid, -pident, -length, -order, -family, -genus, -Additive, -Phase, -Run, -CowName, -Day, -Date, -X..grain.same.day, -Mean.pH.same.day, -Minimum.pH.same.day, -Maximum.pH.same.day, -minutes.pH.6.0.same.day) %>%
  distinct() %>%
  select(sample_detected, percent_sample, everything())
  

df_cor[] <- lapply(df_cor[], function(x) as.numeric(as.character(x)))


mcor <- cor(df_cor ,use="complete.obs")

df_mcor <- data.frame(mcor) 


df_mcor <- df_mcor[order(df_mcor$sample_detected),] 


mcor <- as.matrix(df_mcor)

#library(corrplot)

# Open a pdf file
pdf("~/master/strain_collection/corrplot.pdf", width = 20, height = 15) 
# 2. Create a plot
corrplot(mcor, method = "shade", tl.srt = 25)
# Close the pdf file
dev.off() 

pdf("~/master/strain_collection/minutesPHplot.pdf", width = 20, height = 15) 

plot <- ggplot(df_cor, aes(x=minutes.pH.6.0.whole.Phase, y=percent_sample)) + 
  geom_point() + 
  geom_smooth()
plot

dev.off() 



