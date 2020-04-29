library(tidyverse)

df_regions <- read.csv("~/master/scratch/fragment_ani_1000_500_2_regions.csv")


df_distance <- df_regions %>%
  filter(snp_diff != 0) %>%
  group_by(genome1, genome2, snp_diff) %>%
  mutate(n_frags = length(unique(fragment1))) %>%
  ungroup() %>% 
  
  mutate(distance = 1 / (n_frags / snp_diff)) %>%
  
  select(genome1, genome2, n_frags, snp_diff, distance) %>%
  distinct() %>%
  
  group_by(genome1, genome2) %>%
  top_n(1, (1/distance)) %>%
  ungroup() %>%
  
  select(genome1, genome2, distance) %>%
  
  distinct() 

df_distance_spread <- df_distance %>%
  spread(genome2, distance)

df_distance_spread[is.na(df_distance_spread)] <- 0

df_distance_matrix <- as.matrix(df_distance_spread[,2:ncol(df_distance_spread)])  
row.names(df_distance_matrix) <- df_distance_spread$genome1

distance <- dist(df_distance_matrix) # method="man" # is a bit better
hclust <- hclust(distance, method = "complete")
ord <- hclust$order

# plotting

library(cowplot)
library(scales)

df_distance$genome1 <- factor(df_distance$genome1, levels = rownames(df_distance_matrix)[ord])
df_distance$genome2 <- factor(df_distance$genome2, levels = colnames(df_distance_matrix)[ord])
df_distance$x_holder <- "X"

heatmap_ani <- ggplot(df_distance, aes(genome1, genome2) ) +
  geom_tile(aes(fill = distance)) +
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank(), 
        axis.title.x=element_blank(),
        axis.title.y=element_blank(), 
        legend.position = "none") + 
  scale_fill_gradientn(colors = c("red", "green"),
                       guide = "colourbar",
                       values = rescale(c(0, max(df_distance$distance)))) 

heatmap_ani


