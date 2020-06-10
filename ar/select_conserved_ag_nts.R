library(tidyverse)

# pathogen hits
df_pathogen_hits <- read_csv("~/master/ar/dataflow/04-tables/PATH_hits_100_60.csv")
df_pathogen_count <- read_csv("~/master/ar/dataflow/00-meta/pathogen_genome_count.csv")
colnames(df_pathogen_count)[1] <- 'organism'

pathogens = c('staphylococcus_aureus', 'campylobacter_coli', 'campylobacter_jejuni', 'clostridioides_difficile', 'salmonella_typhimurium', 'salmonella_newport', 'staphylococcus_pseudintermedius', 'streptococcus_agalactiae', 'enterococcus_faecium', 'erysipelothrix_rhusiopathiae', 'streptococcus_suis')

for (pathogen in pathogens){
  df_pathogen_hits[grep(pathogen, df_pathogen_hits$query_file), 'organism'] <- pathogen
}

# card hits
df_card_hits <- read_csv("~/master/ar/dataflow/04-tables/CARD_hits_95_90.csv")
df_card_activities <- read.csv("~/master/ar/dataflow/00-meta/card_annotation_activities.csv")
df_card_activities$card_annotation <- as.character(df_card_activities$card_annotation)

# rumen genomes orf locations
df_rumen_header <- read_csv("~/master/ar/dataflow/04-tables/header_map_rumen_genomes.csv")
colnames(df_rumen_header)[1] <- "query_id"

# look at only the aminoglycoside nucleotidyltransferases
df_ag_nts <- left_join(df_pathogen_hits, df_pathogen_count) %>%
  inner_join(df_rumen_header) %>%
  inner_join(df_card_activities) %>%
  distinct() %>%
  filter(specificity == "aminoglycoside") %>%
  mutate(gene_length = abs(end - start)) %>%
  filter(gene_length > 200)
  #filter(activity == "nucleotidyltransferase" & specificity == "aminoglycoside")

# save dataframe
write.csv(df_ag_nts, "~/master/ar/dataflow/04-tables/aminoglycoside_modifying.csv")

check <- df_ag_nts  %>%
  select(query_id, start, end, card_annotation, gene_family) %>%
  distinct()
