library(tidyverse)

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
  filter(genome1 != genome2) %>%
  mutate(same_host = if_else(host1 == host2, "y", "n")) %>%
  mutate(same_species = if_else(species1 == species2, "y", "n")) %>%
  filter(same_host == "y") %>%
  filter(same_species == "y")

derep_selected_genomes <- unique(df_derep_select$genome2)

df_ani_complete_derep <- df_ani_complete[!(df_ani_complete$genome1 %in% derep_selected_genomes),]
df_ani_complete_derep <- df_ani_complete_derep[!(df_ani_complete_derep$genome2 %in% derep_selected_genomes),]

df_ani_complete_derep_coli_trim <- df_ani_complete_derep %>%
  filter(species1 == "Campylobacter_D coli" & species2 == "Campylobacter_D coli") %>%
  filter(host1 != "housefly") %>%
  filter(host1 != "turkey")

write.csv(df_ani_complete_derep_coli_trim, "~/master/campy/dataflow/00-meta/ani_drep_ccoli_trim.csv", row.names = FALSE)
