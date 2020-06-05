library(tidyverse)

df_pathogen_hits <- read_csv("master/ar/dataflow/04-tables/PATH_hits_99_60.csv")
df_pathogen_count <- read_csv("master/ar/dataflow/00-meta/pathogen_genome_count.csv")
colnames(df_pathogen_count)[1] <- 'organism'

df_headers <- read_csv("master/ar/dataflow/04-tables/header_map_rumen_genomes.csv")
colnames(df_headers)[1] <- c("query_id")

pathogens = c('staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis')


for (pathogen in pathogens){
  df_pathogen_hits[grep(pathogen, df_pathogen_hits$query_file), 'organism'] <- pathogen
}

df_summary <- df_pathogen_hits %>%
  group_by(query_id, organism, card_annotation) %>%
  mutate(n_pathogen_genomes = length(unique(pathogen_genome_id))) %>%
  ungroup() %>%
  select(query_id, genome_id, organism, card_annotation, n_pathogen_genomes) %>%
  distinct() %>%
  left_join(df_pathogen_count) %>%
  mutate(per_genomes = (n_pathogen_genomes / genome_count)*100) %>%
  separate(card_annotation, c("ard", "ard_organism"), sep = " \\[") %>%
  group_by(ard) %>%
  mutate(n_rumen_genomes = length(unique(genome_id))) %>%
  mutate(n_organisms = length(unique(organism))) %>%
  ungroup() %>%
  select(organism, ard, n_pathogen_genomes, per_genomes, n_rumen_genomes, n_organisms) %>%
  distinct()

df_summary$ard_organism <- gsub("\\]", "", df_summary$ard_organism)
