
# rbh ani
df_ani_rbh <- read.csv("~/master/campy/dataflow/00-meta/ani_reciprocal_mean.csv", colClasses = "character")
df_ani_rbh$mean_ani <- as.numeric(df_ani_rbh$mean_ani)

# meta
df_hand <- read.csv("~/master/campy/dataflow/00-meta/campylobacter_sample_attributes_clean_hand.csv")
df_hand$attributes <- NULL

df_acc_map <- read.delim("~/master/campy/dataflow/00-meta/campylobacter_sample_accession_map.txt", header=FALSE)
colnames(df_acc_map) <- c("accession", "biosample")

df_file_map <- read.csv("~/master/campy/dataflow/00-meta/gtdbtk_Campylobacter_D.csv")

df_host_map <- inner_join(df_hand, df_acc_map) %>%
  inner_join(df_file_map)

df_host_map$genome1 <- gsub("_genomic", "_major_contig", df_host_map$file)
df_host_map$genome2 <- gsub("_genomic", "_major_contig", df_host_map$file)

df_host_map$host1 <- df_host_map$host
df_host_map$host2 <- df_host_map$host

df_host_map$species1 <- df_host_map$species
df_host_map$species2 <- df_host_map$species

df_host_map1 <- df_host_map %>%
  select(genome1, host1, species1)

df_host_map2 <- df_host_map %>%
  select(genome2, host2, species2)

# complete

df_ani_complete <- df_ani_rbh %>%
  inner_join(df_host_map1) %>%
  inner_join(df_host_map2)

# replicate

df_derep_select <- df_ani_complete %>%
  filter(mean_ani > 99.9) %>%
  filter(host1 == "human") %>%
  filter(genome1 != genome2) %>%
  mutate(same_host = if_else(host1 == host2, "y", "n")) %>%
  mutate(same_species = if_else(species1 == species2, "y", "n")) %>%
  filter(same_host == "y") %>%
  filter(same_species == "y")

derep_selected_genomes <- unique(df_derep_select$genome2)

df_ani_complete_derep <- df_ani_complete[!(df_ani_complete$genome1 %in% derep_selected_genomes),]
df_ani_complete_derep <- df_ani_complete_derep[!(df_ani_complete_derep$genome2 %in% derep_selected_genomes),]


# clustering 

df_ani_complete_derep_rev <- df_ani_complete_derep
colnames(df_ani_complete_derep_rev) <- gsub("1", "PLACEHOLD", names(df_ani_complete_derep_rev))
colnames(df_ani_complete_derep_rev) <- gsub("2", "1", names(df_ani_complete_derep_rev))
colnames(df_ani_complete_derep_rev) <- gsub("PLACEHOLD", "2", names(df_ani_complete_derep_rev))

df_ani_complete_derep_dup <- bind_rows(df_ani_complete_derep, df_ani_complete_derep_rev)

df_ani_complete_derep_cluster <- df_ani_complete_derep_dup %>%
  select(genome1, genome2, mean_ani) %>%
  filter(genome1 != genome2) %>%
  spread(genome2, mean_ani)

df_ani_complete_derep_cluster_matrix <- as.matrix(df_ani_complete_derep_cluster[,2:ncol(df_ani_complete_derep_cluster)])
row.names(df_ani_complete_derep_cluster_matrix) <- df_ani_complete_derep_cluster$genome1 

distance_ani <- dist(df_ani_complete_derep_cluster_matrix) # method="man" # is a bit better
hclust_ani <- hclust(distance_ani, method = "complete")
ord <- hclust_ani$order

# plotting

library(cowplot)

df_ani_complete_derep_dup$genome1 <- factor(df_ani_complete_derep_dup$genome1, levels = rownames(df_ani_complete_derep_cluster_matrix)[ord])
df_ani_complete_derep_dup$genome2 <- factor(df_ani_complete_derep_dup$genome2, levels = colnames(df_ani_complete_derep_cluster_matrix)[ord])

df_ani_complete_derep_dup$x_holder <- "X"

heatmap_ani <- ggplot(df_ani_complete_derep_dup, aes(genome1, genome2) ) +
  geom_tile(aes(fill = mean_ani)) +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_blank(), 
        axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank(), 
        axis.title.x=element_blank(),
        axis.title.y=element_blank(), 
        legend.position = "none")

heatmap_host <-ggplot(df_ani_complete_derep_dup, aes(x_holder, genome1) ) +
  geom_tile(aes(fill = host1)) +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_blank(), 
        axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank(), 
        axis.title.x=element_blank(),
        axis.title.y=element_blank())

combined_plot <- plot_grid(heatmap_ani, heatmap_host)
