library(tidyverse)

files <- list.files("~/master/campy/dataflow/02-ani/", pattern = ".txt")
list_dfs <- list()
i <- 1

for (file in files){
  
  input <- paste('~/master/campy/dataflow/02-ani/', file, sep = '')
  df <- read.delim(input, header=FALSE)
  df$V4 <- NULL
  df$V5 <- NULL
  
  colnames(df) <- c("genome1", "genome2", "ani")
  df$genome1 <- gsub("dataflow/01-nucl/selected_genomes/", "", df$genome1)
  df$genome2 <- gsub("dataflow/01-nucl/selected_genomes/", "", df$genome2)
  
  
  list_dfs[[i]] <- df
  
  i <- i + 1
}

df_ani_compiled <- bind_rows(list_dfs)

# reciprocal hits

df_forward <- df_ani_compiled %>%
  rename(forward_ani = ani) %>%
  distinct()

df_reverse <- df_ani_compiled %>%
  rename(reverse_ani = ani) %>%
  distinct()

colnames(df_reverse)[1:2] <- c("genome2", "genome1")

df_ani_rbh <- inner_join(df_forward, df_reverse) %>%
  mutate(mean_ani = (forward_ani + reverse_ani)/2) %>%
  select(-forward_ani, -reverse_ani) %>%
  distinct() 

for (row in 1:nrow(df_ani_rbh)){
  ordered_comparison <- sort(c(df_ani_rbh$genome1[row], df_ani_rbh$genome2[row]))
  comparison_sep <- paste(ordered_comparison[1], ordered_comparison[2], sep = ";")
  df_ani_rbh$comparison[row] <- comparison_sep
}

df_ani_rbh <- df_ani_rbh %>%
  select(-genome1, -genome2) %>%
  distinct() %>%
  separate(comparison, into = c("genome1", "genome2"), sep = ";")

write.csv(df_ani_rbh, "~/master/campy/dataflow/00-meta/ani_reciprocal_mean.csv", row.names = FALSE)