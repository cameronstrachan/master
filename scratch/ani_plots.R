library(tidyverse)

library(ggthemes)

df <- read.csv("~/master/scratch/popani_100_9.csv")

df <- df %>%
  filter(genome1 == "GCF_001417635.1_ASM141763v1_major_contig") %>%
  filter(genome2 == "GCF_002024185.1_ASM202418v1_major_contig" | genome2 == "GCF_000583795.1_ASM58379v1_major_contig") %>%
  mutate(ani_diff = fragment_ani - genome_wide_ani) 


# Plot
ggplot(df, aes(x=fragment1, y=ani_diff, colour=genome2)) +
  geom_line(size=0.2, alpha=0.9, linetype=2) 
