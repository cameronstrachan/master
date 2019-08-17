library(tidyverse)
library(string)

df_annotations <- read.csv("~/master/anna/dataflow/03-tables/compiled_nr_blast.txt")

df_annotations <- df_annotations %>% 
  select(X, sseq_description, percent_identity, hit_num) %>%
  separate(sseq_description, into = c("annotation", "taxa"), sep = '\\[') %>%
  select(-taxa, -hit_num, -percent_identity) %>%
  distinct() %>% 
  group_by(X) %>%
  mutate(annotations = as.character(list(annotation))) %>%
  ungroup() %>%
  select(-annotation) %>%
  distinct() %>%
  separate(X, into = c("qseqid", "rm"), sep = '_e') %>%
  select(-rm)

df_annotations$annotations <- gsub('c\\(', '', df_annotations$annotations)
df_annotations$annotations <- gsub('\\)', '', df_annotations$annotations)

df_genes <- read.csv("~/master/anna/extracted_regions_genes.csv")

df_final <- df_genes %>%
  select(-X) %>%
  left_join(df_annotations)

write.csv(df_final, "~/master/anna/annotated_regions.csv")
