library(tidyverse)

taxonomy_7_levels <- read.delim("~/master/wolf/dataflow/00-databases/taxonomy_7_levels.txt", header=FALSE)

colnames(taxonomy_7_levels) <- c("accession", "taxa_levels")

df <- taxonomy_7_levels %>%
  separate(taxa_levels, into = c("Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species"), sep = ";") %>%
  filter(Order == "D_3__Betaproteobacteriales") %>%
  filter(Family == "D_4__Neisseriaceae")

write.csv(df, "~/master/strain_collection/betaprot_silva_seqs.csv")


df_names <- read.csv("~/master/strain_collection/beta_first_tree_names.csv", sep=",")

df_names <- df_names %>%
  separate(names, into = ("accession"), remove = FALSE, sep = "_")

df_rename <- df %>%
  select(accession, Family, Genus, Species) %>%
  full_join(df_names)


df_rename$Family[is.na(df_rename$Family)] <- "blast"
df_rename$Genus[is.na(df_rename$Genus)] <- "hit"

df_rename$Family[df_rename$names == "2019_08_19_9_1492R_88_extraction_(reversed)"] <- "clone"
df_rename$Genus[df_rename$names == "2019_08_19_9_1492R_88_extraction_(reversed)"] <- "9"

df_rename$Family[df_rename$names == "2019_08_19_40_1492R_90_extraction_(reversed)"] <- "clone"
df_rename$Genus[df_rename$names == "2019_08_19_40_1492R_90_extraction_(reversed)"] <- "40"

df_rename$Family[df_rename$names == "2019_08_19_12_1492R_81_extraction_(reversed)"] <- "clone"
df_rename$Genus[df_rename$names == "2019_08_19_12_1492R_81_extraction_(reversed)"] <- "12"

df_rename$Family <- gsub("D_4__", "", df_rename$Family)
df_rename$Genus <- gsub("D_5__", "", df_rename$Genus)
df_rename$Species <- gsub("D_6__", "", df_rename$Species)

df_rename <- df_rename %>%
  unite(rename, c("Family", "Genus", "accession"), sep = "_")

write.csv(df_rename, "~/master/strain_collection/tree_rename_beta.csv")
