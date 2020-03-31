library(tidyverse)

tree <- read.csv("~/master/epsilon/dataflow/02-classification/gtdbtk.bac120.user_msa.fasta.treefile", header=FALSE, sep=" ")
tree <- as.character(tree$V1)

class <- read.delim("~/master/epsilon/dataflow/02-classification/gtdbtk.bac120.summary.tsv")

class <- class %>%
  select(user_genome, classification) %>%
  separate(classification, into = c("L1", "L2", "L3", "L4", "L5", "L6", "L7"), sep = ";") %>%
  select(user_genome, L6, L7)

class$L6 <- gsub("g__", "", class$L6)
class$L6 <- gsub(" ", "_", class$L6)
class$L7 <- gsub("s__", "", class$L7)
class$L7 <- gsub(" ", "_", class$L7)
class$label <- gsub("_genomic", "", class$user_genome)


df_label <- class %>%
  unite(label, c("L6", "L7", "label"), sep = "_", remove = FALSE)

for (x in 1:nrow(df_label)){
  tree_label <- as.character(df_label[x, "user_genome"])
  new_label <- as.character(df_label[x, "label"])
  tree <- gsub(tree_label, new_label, tree)
}

df_A <- df_label %>%
  filter(L6 == "Campylobacter_A")
