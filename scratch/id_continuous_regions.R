library(tidyverse)

### combine host data and trim data
frag_length <- 10000

df <- read.csv("~/master/scratch/fragment_ani_1000.csv")
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

# may need to adjust the rounding to get most accurate or conservative snp value

df <- df %>%
  filter(genome1 != genome2) %>%
  mutate(ani_diff = fragment_ani - genome_wide_ani) %>%
  left_join(meta1) %>%
  left_join(meta2) %>%
  mutate(fragment_snps = round((1 - (fragment_ani/100)) * fragment_size1)) %>%
  mutate(genome_wide_snps = round((1 - (genome_wide_ani/100)) * fragment_size1)) %>%
  mutate(snp_diff = genome_wide_snps - fragment_snps) %>%
  filter(snp_diff > 0 )


### make region dataframes

region_dfs_list <- list()
genomes <- unique(df$genome1)
l <- 1

for (genome in genomes){
  
  df_single_genome <- df %>%
    filter(genome1 == genome)
  comparisons <- unique(df$genome2)
  
  for (comparison in comparisons){
    
    # this is only sorting and then finding a contious stretch of fragment numbers (more than 3) with the same number of snps
    # i could fix this code to get regions with a window of snips, but then the basic ordering would not work
    # therefore, the code is looking for adjacent regions with the same snps per frag length
    # this of course finds first regions where adjacent the fragments are all 100% ANI to the most distant genome 
    
    df_single_comparison <-  df_single_genome %>%
      filter(genome2 == comparison) %>%
      arrange(desc(snp_diff))
    
    
    
    continous_regions <- split(df_single_comparison$fragment1, cumsum(c(1, diff(df_single_comparison$fragment1) != 1)))
    continous_regions <- continous_regions[lapply(continous_regions, length) > 15]
    
    
    if (length(continous_regions) > 0) {
      
      c <- 1
      
      for (i in 1:length(continous_regions)){
        df_regions <- as.data.frame(continous_regions[i])
        
        colnames(df_regions) <- "fragment1"
        df_regions$genome1 <- genome
        df_regions$genome2 <- comparison
        df_regions$region1 <- i
        region_dfs_list[[l]] <- df_regions
        
        c <- c + 1
        l <- l + 1
        
      }
    }
  }
}

df_regions <- bind_rows(region_dfs_list)

df_final <- inner_join(df, df_regions) %>%
  group_by(genome1, genome2, region1) %>%
  mutate(n_fragsment = length(unique(fragment1))) %>%
  mutate(mean_fragments = mean(snp_diff)) %>%
  ungroup()


library(ggthemes)

p1 <- ggplot(df_final, aes(x = fragment1, y = snp_diff, colour = host2)) +
  geom_point() +
  facet_wrap(host1 ~ genome1) +
  theme_minimal()

p1
