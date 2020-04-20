library(tidyverse)

df_complete <- read.csv("~/master/epsilon/dataflow/00-meta/complete_coli_jejuni_meta.csv")
df_complete$X <- NULL
df_complete$accession <- as.character(df_complete$accession)

df_mapping <- read.delim("~/master/epsilon/dataflow/00-meta/isolation_mapping_file.txt", header=FALSE)
colnames(df_mapping) <- c("accession", "biosample")
df_mapping$accession <- as.character(df_mapping$accession)
df_mapping$biosample <- as.character(df_mapping$biosample)

df_final <- inner_join(df_complete, df_mapping) 

command <- "esearch -db biosample -q 'SAMN02743856' | esummary | xtract -pattern DocumentSummary -element Attribute"

x <- system2(command, stdout=TRUE)

