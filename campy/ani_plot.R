library(tidyverse)

files <- list.files("~/master/campy/dataflow/02-ani/", pattern = ".txt")
list_dfs <- list()
i <- 1

for (file in files){
  
  input <- paste('~/master/campy/dataflow/02-ani/', file, sep = '')
  df <- read.delim(input, header=FALSE)
  df$V4 <- NULL
  df$V5 <- NULL
  
  colnames(df) <- c("genome1", "genome2", "ani")
  df$genome1 <- gsub("dataflow/01-nucl/selected_genomes/", "", df$genome1)
  df$genome2 <- gsub("dataflow/01-nucl/selected_genomes/", "", df$genome2)
  
  #df <- df %>%
  #  spread(genome2, ani)
  
  list_dfs[[i]] <- df
  
  i <- i + 1
}

df_ani_final <- bind_rows(list_dfs)


# meta
df_hand <- read.csv("~/master/campy/dataflow/00-meta/campylobacter_sample_attributes_clean_hand.csv")
df_hand$attributes <- NULL

df_acc_map <- read.delim("~/master/campy/dataflow/00-meta/campylobacter_sample_accession_map.txt", header=FALSE)
colnames(df_acc_map) <- c("accession", "biosample")

df_file_map <- read.csv("~/master/campy/dataflow/00-meta/gtdbtk_Campylobacter_D.csv")

df_host_map <- inner_join(df_hand, df_acc_map) %>%
  inner_join(df_file_map)

df_host_map$genome1 <- gsub("_genomic", "_major_contig", df_host_map$file)

###

df_ani_cluster <- df_ani_final %>%
  inner_join(df_host_map)

df_ani_cluster_spread <- df_ani_cluster %>%
  select(genome1, species, host, genome2, ani) %>%
  spread(genome2, ani)

df_ani_cluster_matrix <- as.matrix(df_ani_cluster_spread[,4:ncol(df_ani_cluster_spread)])
rownames(df_ani_cluster_matrix) <- df_ani_cluster_spread$genome1

distance_ani <- dist(df_ani_cluster_matrix) # method="man" # is a bit better
hclust_ani <- hclust(distance_ani, method = "complete")
ord <- hclust_ani$order

df_ani_cluster$genome1 <- factor(df_ani_cluster$genome1, levels = rownames(df_ani_cluster_matrix)[ord])
df_ani_cluster$genome2 <- factor(df_ani_cluster$genome2, levels = colnames(df_ani_cluster_matrix)[ord])

heat1 <- ggplot(df_ani_cluster, aes(genome1, genome2) ) +
  geom_tile(aes(fill = ani)) +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_blank())

ggplot(df_ani_cluster, aes(species,genome1) ) +
  geom_tile(aes(fill = host)) +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_blank())
