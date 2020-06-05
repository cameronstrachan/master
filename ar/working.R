library(tidyverse)

df_pathogen_hits <- read_csv("~/master/ar/dataflow/04-tables/PATH_hits_99_60.csv")
df_pathogen_count <- read_csv("~/master/ar/dataflow/00-meta/pathogen_genome_count.csv")
colnames(df_pathogen_count)[1] <- 'organism'

pathogens = c('staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis')

for (pathogen in pathogens){
  df_pathogen_hits[grep(pathogen, df_pathogen_hits$query_file), 'organism'] <- pathogen
}

df_pathogen_hits <- left_join(df_pathogen_hits, df_pathogen_count)

df_rumen_header <- read_csv("~/master/ar/dataflow/04-tables/header_map_rumen_genomes.csv")
colnames(df_rumen_header)[1] <- "query_id"

df_complete <- inner_join(df_pathogen_hits, df_rumen_header) %>%
  distinct() #%>%
  select(query_id, card_annotation, start, end, direction, subject_id, organism, genome_count, subject_start, subject_end, percent_identity, percent_alignment, )
