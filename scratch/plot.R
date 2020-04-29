library(tidyverse)

library(ggthemes)

df_regions <- read.csv("~/master/scratch/popani_100_5_regions.csv")

df_regions_trim <- df_regions %>%
  filter(n_continuous_frags >= 40)

### meta data
meta <- read.csv("~/master/scratch/meta.csv", colClasses = "character")

meta1 <- meta %>% select(file, host)
meta1$host1 <- meta1$host
meta1$host <- NULL
meta1$genome1 <- gsub(".fna", "", meta1$file)
meta1$file <- NULL

meta2 <- meta1
colnames(meta2) <- c('host2', 'genome2')

###

df_plot <- df_regions_trim %>%
  inner_join(meta1) %>%
  inner_join(meta2)

###

p1 <- ggplot(df_plot, aes(x = fragment1, y = snp_diff, colour = host2)) +
  geom_point() +
  facet_wrap(host1 ~ genome1) +
  theme_minimal()

p1
