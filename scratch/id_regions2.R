library(tidyverse)


df <- read.csv("~/master/scratch/fragment_ani_1000.csv")
df$genome1 <- as.character(df$genome1)
df$genome2 <- as.character(df$genome2)

df_snp <- df %>%
  filter(genome1 != genome2) %>%
  mutate(ani_diff = fragment_ani - genome_wide_ani) %>% 
  mutate(fragment_snps = round((1 - (fragment_ani/100)), 3) * fragment_size1) %>%
  mutate(genome_wide_snps = round((1 - (genome_wide_ani/100)), 3) * fragment_size1) %>%
  mutate(snp_diff = genome_wide_snps - fragment_snps) %>%
  filter(snp_diff >= 0)

region_dfs_list <- list()
genomes <- unique(df$genome1)
l <- 1

for (genome in genomes){
  
  df_genome1 <- df_snp %>%
    filter(genome1 == genome)
    
  comparisons <- unique(df_genome1$genome2)
  
  for (comparison in comparisons){
    
    df_single_comparison <-  df_genome1 %>%
      filter(genome2 == comparison) %>%
      arrange(desc(snp_diff))
    
    continous_regions <- split(df_single_comparison$fragment1, cumsum(c(1, diff(df_single_comparison$fragment1) != 1)))

    if (length(continous_regions) > 0) {
      
      for (i in 1:length(continous_regions)){
        df_regions <- as.data.frame(continous_regions[i])
        colnames(df_regions) <- "fragment1"
        df_regions$n_continuousfrags_at_snplvl_per_genome = nrow(df_regions)
        df_regions$genome1 <- genome
        df_regions$genome2 <- comparison
        df_regions$region1 <- i
  
        region_dfs_list[[l]] <- df_regions
        
        l <- l + 1
        
      }
    }
  }
}

df_regions <- bind_rows(region_dfs_list)
 
df_final <- inner_join(df_snp, df_regions) %>%
  # number genomes with this region 0 or above per fragment
  group_by(genome1, fragment1) %>%
  mutate(n_genome_per_frag = length(unique(genome2))) %>%
  ungroup() %>%
  
  # number of fragments at level of snps per genome
  group_by(genome1, snp_diff, genome2) %>%
  mutate(n_frags_at_snplvl_per_genome = length(unique(fragment1))) %>%
  ungroup()

## meta data
meta <- read.csv("~/master/scratch/meta.csv", colClasses = "character")

meta1 <- meta %>% select(file, host)
meta1$host1 <- meta1$host
meta1$host <- NULL
meta1$genome1 <- gsub(".fna", "", meta1$file)
meta1$file <- NULL

meta2 <- meta1
colnames(meta2) <- c('host2', 'genome2')

## plot
df_plot <- df_final %>%
  filter(n_continuousfrags_at_snplvl_per_genome >= 15) %>%
  inner_join(meta1) %>%
  inner_join(meta2) %>%
  filter(host2 == "cattle")


      
library(ggthemes)

p1 <- ggplot(df_plot, aes(x = fragment1, y = snp_diff, colour = genome2)) +
  geom_point() +
  facet_wrap(host1 ~ genome1) +
  theme_minimal()

p1


df_check <- df_plot 
