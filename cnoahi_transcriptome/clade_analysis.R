library(tidyverse)

df_clade <- read.csv("~/master/chyo/clade_structure.csv")
df_classification <- read.delim("~/master/chyo/gtdbtk.bac120.summary.tsv")

df_classification <- df_classification %>%
  select(user_genome, classification)

df_combined <- inner_join(df_classification, df_clade)

df_combined$classification <- gsub("d__Bacteria;p__Campylobacterota;c__Campylobacteria;o__Campylobacterales;f__Campylobacteraceae;", "", df_combined$classification)

df_combined <- df_combined %>%
  separate(classification, into = c("genus", "species"), sep = ';')

df_combined$species <- gsub("s__", "", df_combined$species)
df_combined$species <- gsub("Campylobacter", "", df_combined$species)
df_combined$species <- gsub("_A ", "", df_combined$species)
df_combined$species <- gsub("_B ", "", df_combined$species)
df_combined$species <- gsub("_D ", "", df_combined$species)
df_combined$genus <- gsub("g__", "", df_combined$genus)

df_combined_species_list <- df_combined %>%
  select(-user_genome) %>%
  distinct() %>%
  group_by(genus, clade) %>%
  summarise(species = list(species)) %>%
  ungroup()

df_combined_species_list$species <- as.character(df_combined_species_list$species)
df_combined_species_list$species <- gsub("c\\(\"", "", df_combined_species_list$species)
df_combined_species_list$species <- gsub("\"", "", df_combined_species_list$species)


write.csv(df_combined_species_list, '~/master/chyo/species_clade_summary.csv')
