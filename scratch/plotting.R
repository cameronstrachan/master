library(tidyverse)

df <- read.csv("~/master/scratch/fragment_ani.csv")
df$genome1 <- as.character(df$genome1)
df$genome2 <- as.character(df$genome2)

meta <- read.csv("~/master/scratch/meta.csv", colClasses = "character")

meta1 <- meta %>% select(file, host)
meta1$host1 <- meta1$host
meta1$host <- NULL
meta1$genome1 <- gsub(".fna", "", meta1$file)
meta1$file <- NULL

meta2 <- meta1
colnames(meta2) <- c('host2', 'genome2')


df <- df %>%
  filter(genome1 != genome2) %>%
  mutate(ani_diff = fragment_ani - genome_wide_ani) %>%
  left_join(meta1) %>%
  left_join(meta2) %>%
  filter(ani_diff > 0) %>%
  filter(host1 != "chicken")
  
library(ggthemes)

p1 <- ggplot(df, aes(x = fragment1, y = ani_diff, colour = genome2)) +
  geom_point() +
  facet_wrap(host1 ~ genome1, scales = "free_x") +
  theme_minimal()
  
p1

  
