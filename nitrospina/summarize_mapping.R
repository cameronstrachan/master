library(tidyverse)

files <- list.files("~/master/nitrospina/dataflow/03-sam-counts/")
file_list <- list()
i <- 1

for (file in files){
  acc <- gsub("_all_nitrospina_genomes.txt", "", file)
  file_path <- paste("~/master/nitrospina/dataflow/03-sam-counts/", file, sep = "")
  df <- read.delim(file_path, header=FALSE)
  df$V1 <- NULL
  df$accession <- acc
  file_list[[i]] <- df
  i <- i + 1
}

df <- bind_rows(file_list) %>%
  filter(V2 != "") %>%
  filter(V2 != "1_195") %>%
  filter(V3 >= 2)

colnames(df)[1:2] <- c("ID", "Count")

df_gff3 <- read.delim("~/master/nitrospina/dataflow/01-prot/genes/all_nitrospina_genomes.gff3", header=FALSE, comment.char="#")

df_gff3 <- df_gff3 %>%
  separate(V9, sep = ";", into = c("ID"))

df_gff3$ID <- gsub("ID=", "", df_gff3$ID)

df_gff3 <- df_gff3 %>%
  inner_join(df) %>%
  select(V1, V4, V5, V7, ID, Count, accession) 

colnames(df_gff3)[1:4] <- c("contig", "start", "end", "direction")

df_gff3 <- df_gff3 %>%
  filter(contig != "Ecoli_1")

write.csv(df_gff3, "~/master/nitrospina/dataflow/00-meta/all_nitrospina_genomes.csv")

