library(tidyverse)

taxonomy_7_levels <- read.delim("/Volumes/CamExternal/master_backup_july24-2019/master/wolf/dataflow/00-databases/taxonomy_7_levels.txt", header=FALSE)

colnames(taxonomy_7_levels) <- c("accession", "taxa_levels")

df <- taxonomy_7_levels %>%
  separate(taxa_levels, into = c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species"), sep = ";") %>%
  filter(Phylum == "D_1__Actinobacteria") %>%
  filter(Order == "D_3__Actinomycetales")

write.csv(df, "~/master/strain_collection/actinobacteria_silva_seqs.csv")


df_names <- read.csv("~/master/strain_collection/actinos_with_outgroup_full_coverage_tree_names.csv", sep=",")

df_names <- df_names %>%
  separate(names, into = ("accession"), remove = FALSE, sep = "_")

df_rename <- df %>%
  select(accession, Family, Genus, Species) %>%
  full_join(df_names)


df_rename$Family[is.na(df_rename$Family)] <- "Goat"
df_rename$Genus[is.na(df_rename$Genus)] <- "clone"
df_rename$Species[is.na(df_rename$Species)] <- "wetzels"

df_rename$Family[df_rename$accession == "i21"] <- "i21"
df_rename$Genus[df_rename$accession == "i21"] <- "isolate"
df_rename$Species[df_rename$accession == "i21"] <- "strachan"

df_rename$Family <- gsub("D_4__", "", df_rename$Family)
df_rename$Genus <- gsub("D_5__", "", df_rename$Genus)
df_rename$Species <- gsub("D_6__", "", df_rename$Species)

df_rename <- df_rename %>%
  unite(rename, c("Family", "Genus", "accession"), sep = "_")

write.csv(df_rename, "~/master/strain_collection/tree_rename.csv")
