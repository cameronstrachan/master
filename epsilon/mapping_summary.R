library(tidyverse)

files <- list.files("~/master/epsilon/dataflow/03-sam/", pattern = ".txt")
df_list <- list()
i <- 1

for (file in files){
  file_loc <- paste("~/master/epsilon/dataflow/03-sam/", file, sep = "")
  df <- read.delim(file_loc, header=FALSE)
  colnames(df) <- c("id", "gene", "count")
  
  non_mapped <- max(df$count)
  
  df$file <- file 
  df$unmapped <- non_mapped
  df_list[[i]] <- df
  i <- i + 1
}

df_comp <- bind_rows(df_list) %>%
  filter(id != "__not_aligned") %>%
  filter(id != "__ambiguous") %>%
  filter(id != "__no_feature") %>%
  filter(id != "__too_low_aQual") %>%
  group_by(file) %>%
  mutate(total = sum(count)) %>%
  ungroup()

df_total <- df_comp %>%
  select(file, total, unmapped) %>%
  distinct() %>%
  mutate(percent = (total / unmapped)*100)

write.csv(df_comp, "dataflow/04-analysis-tables/mapped_genes.csv")
write.csv(df_total, "dataflow/04-analysis-tables/mapped_total.csv")
