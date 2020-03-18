library(tidyverse)

meta <- read.csv("~/master/epithelial/dataflow/00-meta/sample_mapping.csv")
meta[] <- lapply(meta, as.character)

counts <- read.delim("~/master/epithelial/dataflow/03-asv-table/neubauer2018_wetzels2017_99.txt", header=FALSE)
counts <- counts[-1,]
counts[] <- lapply(counts, as.character)
names(counts) <- counts[1,]
counts <- counts[-1,]
counts[,2:57] <- lapply(counts[,2:57], as.numeric)
names(counts)[1] <- "asv"

classification <- read.csv("~/master/epithelial/dataflow/04-classification/classification.csv")
classification$X <- NULL

classification <- classification %>%
  select(fasta_header, phylum)

colnames(classification)[1] <- 'asv'

df_data <- gather(counts, ID, count, -asv) %>%
  inner_join(meta) %>% 
  inner_join(classification) %>%
  group_by(ID) %>%
  mutate(reads= sum(count)) %>%
  ungroup() %>%
  mutate(counts_normalized = (count / reads)*100)

df_phylum <- df_data %>%
  
  group_by(Type) %>%
  mutate(total_reads_group = sum(count)) %>%
  ungroup() %>%
  
  group_by(Type, phylum) %>%
  mutate(total_reads_phylum = sum(count)) %>%
  ungroup() %>%
  
  mutate(rel_phy_group = (total_reads_phylum / total_reads_group) *100) %>%
  select(Type, phylum, rel_phy_group) %>%
  distinct()


ggplot(data=df_phylum, 
           aes(x=Type,
               y=rel_phy_group,
               fill=phylum)) + 
  geom_bar(position="fill", stat="identity") + 
  coord_polar(theta='y')
