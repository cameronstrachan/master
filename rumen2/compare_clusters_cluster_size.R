library(tidyverse)

df <- read.csv('~/master/rumen2/dataflow/03-analysis/compiled_start_stop.txt')

df <- df %>%
  mutate(pathogen_centroid = ((pathogen_end_dir - pathogen_start_dir)/2) + pathogen_start_dir) %>%
  mutate(rumen_centroid = ((rumen_end_dir - rumen_start_dir)/2) + rumen_start_dir) %>%
  select(-X) %>%
  distinct()

df_pathogen <- df %>%
  select(ard, pathogen, pathogen_genome_id, pathogen_centroid, pathogen_start_dir, pathogen_end_dir) %>%
  distinct() %>%
  group_by(pathogen, pathogen_genome_id) %>%
  mutate(num_ards = length(unique(ard))) %>%
  ungroup() %>%
  filter(num_ards > 1) %>% 
  distinct() 

df_pathogen$pathogen_genome_id <- as.character(df_pathogen$pathogen_genome_id)

contigs <- unique(df_pathogen$pathogen_genome_id)

df_contig_list <- list()
k <- 1
cluster_num <- 1

for (contig in contigs){
  
  cluster_num <- cluster_num + 1
  
  df_contig <- df_pathogen %>%
    filter(pathogen_genome_id == contig) %>% 
    arrange(pathogen_centroid)
  
  
  
  for (x in 1:nrow(df_contig)){
    num_rows =nrow(df_contig)
    
    if (x == num_rows){ 
      df_contig[x, 'cluster'] <- cluster_num
      next }
    
    j <- x + 1
    one_row_down <- df_contig[j, "pathogen_centroid"]
    start_plus_10kb <- df_contig[x, "pathogen_centroid"] + 5000
    
    if (one_row_down < start_plus_10kb) {
      df_contig[x, 'cluster'] <- cluster_num
    } else {
      cluster_num <- cluster_num + 1
      df_contig[x, 'cluster'] <- cluster_num
    }
    
    
    
  }
  
  df_contig_list[[k]] <- df_contig
  k <- k + 1
   
  
}

df_pathogen_grouped_cluster <- bind_rows(df_contig_list) %>%
  group_by(pathogen_genome_id, cluster) %>%
  mutate(cluster_type = list(sort(unique(as.character(ard))))) %>%
  mutate(num_genes_cluster = length(unique(ard))) %>%
  mutate(cluster_start = min(pathogen_start_dir)) %>%
  mutate(cluster_end = max(pathogen_end_dir)) %>% 
  mutate(cluster_size = cluster_end - cluster_start) %>%
  ungroup() %>%
  filter(num_genes_cluster > 1) %>%
  filter(cluster_size < 10000) %>%
  select(ard, pathogen, cluster_type, cluster_size)

df_pathogen_grouped_cluster$cluster_type <- as.character(df_pathogen_grouped_cluster$cluster_type)
df_pathogen_grouped_cluster$cluster_type <- gsub("c\\(", "", df_pathogen_grouped_cluster$cluster_type)
df_pathogen_grouped_cluster$cluster_type <- gsub("\\)$", "", df_pathogen_grouped_cluster$cluster_type)
df_pathogen_grouped_cluster$cluster_type <- gsub("\"", "", df_pathogen_grouped_cluster$cluster_type)

df_pathogen_grouped_cluster <- df_pathogen_grouped_cluster %>%
  select(-ard) %>%
  distinct()

##

library(stringi)

df <- read.csv('~/master/rumen2/dataflow/03-analysis/compiled_start_stop.txt')

df <- df %>%
  mutate(pathogen_centroid = ((pathogen_end_dir - pathogen_start_dir)/2) + pathogen_start_dir) %>%
  mutate(rumen_centroid = ((rumen_end_dir - rumen_start_dir)/2) + rumen_start_dir) %>%
  select(-X) %>%
  distinct() 

df$rumen_genome_id <- NA

for (i in 1:nrow(df)){
  df[i,"rumen_genome_id"] <- stri_reverse(str_split_fixed(stri_reverse(df[i,"gene_name"]), "_", 3)[[3]])
}

df$rumen <- 'rumen'

df_rumen <- df %>%
  select(ard, rumen, rumen_genome_id, rumen_centroid, rumen_start_dir, rumen_end_dir) %>%
  distinct() %>%
  group_by(rumen, rumen_genome_id) %>%
  mutate(num_ards = length(unique(ard))) %>%
  ungroup() %>%
  filter(num_ards > 1) %>% 
  distinct() 

df_rumen$rumen_genome_id <- as.character(df_rumen$rumen_genome_id)

contigs <- unique(df_rumen$rumen_genome_id)

df_contig_list <- list()
k <- 1
cluster_num <- 1

for (contig in contigs){
  
  cluster_num <- cluster_num + 1
  
  df_contig <- df_rumen %>%
    filter(rumen_genome_id == contig) %>% 
    arrange(rumen_centroid)
  
  
  
  for (x in 1:nrow(df_contig)){
    num_rows =nrow(df_contig)
    
    if (x == num_rows){ 
      df_contig[x, 'cluster'] <- cluster_num
      next }
    
    j <- x + 1
    one_row_down <- df_contig[j, "rumen_centroid"]
    start_plus_10kb <- df_contig[x, "rumen_centroid"] + 5000
    
    if (one_row_down < start_plus_10kb) {
      df_contig[x, 'cluster'] <- cluster_num
    } else {
      cluster_num <- cluster_num + 1
      df_contig[x, 'cluster'] <- cluster_num
    }
    
    
    
  }
  
  df_contig_list[[k]] <- df_contig
  k <- k + 1
  
  
}

df_rumen_grouped_cluster <- bind_rows(df_contig_list) %>%
  group_by(rumen_genome_id, cluster) %>%
  mutate(cluster_type = list(sort(unique(as.character(ard))))) %>%
  mutate(num_genes_cluster = length(unique(ard))) %>%
  mutate(cluster_start = min(rumen_start_dir)) %>%
  mutate(cluster_end = max(rumen_end_dir)) %>% 
  mutate(cluster_size = cluster_end - cluster_start) %>%
  ungroup() %>%
  filter(num_genes_cluster > 1) %>%
  filter(cluster_size < 10000) %>%
  select(ard, rumen, cluster_type, cluster_size)

df_rumen_grouped_cluster$cluster_type <- as.character(df_rumen_grouped_cluster$cluster_type)
df_rumen_grouped_cluster$cluster_type <- gsub("c\\(", "", df_rumen_grouped_cluster$cluster_type)
df_rumen_grouped_cluster$cluster_type <- gsub("\\)$", "", df_rumen_grouped_cluster$cluster_type)
df_rumen_grouped_cluster$cluster_type <- gsub("\"", "", df_rumen_grouped_cluster$cluster_type)

df_rumen_grouped_cluster <- df_rumen_grouped_cluster %>%
  select(-ard) %>%
  distinct()

#

colnames(df_pathogen_grouped_cluster)[1] <- "source"
colnames(df_rumen_grouped_cluster)[1] <- "source"

df_final <- bind_rows(df_rumen_grouped_cluster, df_pathogen_grouped_cluster)

df_final_4genes <- df_final %>% 
  
  group_by(source) %>%
  mutate(num_cluster_types = length(unique(cluster_type))) %>%
  ungroup() %>%
  
  group_by(source, cluster_type) %>%
  mutate(cluster_variants = length(unique(cluster_size))) %>%
  ungroup() #%>%
 
  #mutate(aada = if_else(grepl("aad\\(6\\)", cluster_type), "yes", "no")) %>%
  #mutate(aph = if_else(grepl("APH\\(3'\\)-IIIa", cluster_type), "yes", "no")) %>%
  #mutate(aada_b = if_else(grepl("ANT\\(6\\)-Ib", cluster_type), "yes", "no")) %>%
  #mutate(sat = if_else(grepl("SAT-4", cluster_type), "yes", "no")) %>%
  #gather(gene, gene_presence, -source, -cluster_type, -cluster_size, -cluster_variants, -num_cluster_types) %>%
  #filter(gene_presence != "no")
  

#

plot <- ggplot(df_final_4genes, aes(x=num_cluster_types)) +
  theme_gdocs() +
  geom_jitter(aes(y = cluster_variants, colour = cluster_type, shape = source),
             stat = "identity", fill = "lightgrey", size = 2, width = 0.4) +
  theme(strip.text = element_text(size = 14),
        axis.text.y = element_text(size = 14), 
        axis.title.y = element_text(size = 16),
        axis.text.x = element_text(angle = 90, hjust = 1, size = 14)) +
  ylab("Number variants") +
  xlab("Number unique cluster") +
  scale_shape_manual(values=c(15, 16, 17, 18))#+
  #facet_grid(. ~ source)

plot

#

