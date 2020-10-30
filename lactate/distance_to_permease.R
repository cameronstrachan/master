library(tidyverse)

# user defined
distance_to_permease = 10000
file_extension = '.fa'

# input data from annotate_lactate_metabolism.py (runs compile_lactate_annotations.R)
# compiled blast and hmmer results
compiled <- read.csv("~/master/lactate/dataflow/04-analysis-tables/compiled_lactate_annotations.csv")
compiled$characterized_protein <- as.character(compiled$characterized_protein)
# meta data for characterized protein DB
meta <- read.csv("~/master/lactate/dataflow/00-meta/characterized_protein_annotation.csv")
meta$characterized_protein <- as.character(meta$characterized_protein)
# hmmer results for characterized protein DB
characterized_domains <- read.csv("~/master/lactate/dataflow/04-analysis-tables/characterized_domains.csv")
colnames(characterized_domains)[3] <- "characterized_protein"

# combine meta data and hmmer results for characterized protein DB
meta_domains <- inner_join(meta, characterized_domains) %>%
  select(-hmm_pfam, -hmm_evalue) %>%
  
  # count number of hmm domains found for each characterized protein
  group_by(characterized_protein) %>%
  mutate(n_domains_characterized = length(unique(hmm_domain))) %>%
  ungroup()

# inner join all dataframes from above
# as this joins on the characterized protein id and the hmm domains, 
# proteins that have other domains not in the characterized proteins are excluded 
compiled_annotations <- inner_join(compiled, meta_domains) %>%
  
  # ensure that the proteins have the same number of domains as the characterized proteins
  group_by(gene_id) %>%
  mutate(n_domains = length(unique(hmm_domain))) %>%
  ungroup() %>%
  
  filter(n_domains == n_domains_characterized) 
  
  
# convert gene names, gene ids and genomes to character 
compiled_annotations$gene <- as.character(compiled_annotations$gene)
compiled_annotations$gene_id <- as.character(compiled_annotations$gene_id)
compiled_annotations$genome <- as.character(compiled_annotations$genome)

# split out contig name and gene number
compiled_annotations <- compiled_annotations %>% 
  extract(gene_id, c("contig_id","gene_num"), "(.*)_([^_]+)$", remove = FALSE)


# create a dataframe for only the permeases (our 'anchor gene')
# we will ultimate compare distances to all permeases
permease <- compiled_annotations %>%
  
  # select permeases
  filter(hmm_domain == "Lactate_perm") %>%
  
  # calculate number of permeases
  group_by(genome) %>%
  mutate(n_permease = length(unique(gene_id))) %>%
  ungroup() %>%
  
  # select only the best hit for every single protein (permease)
  group_by(genome, gene_id) %>%
  mutate(max_bitscore = max(bitscore)) %>%
  ungroup() %>%
  
  filter(bitscore == max_bitscore) %>%
  
  # remove annotation and scoring columns
  # how good of hit for a permease won't be used, as we will later determine what other lactate utilization genes are in context 
  select(-characterized_protein, -blast_pident, -blast_per_aln, -bitscore, -max_bitscore, -hmm_domain, -hmm_evalue, -n_domains_characterized, -n_domains) %>%
  
  # calculate the middle of the permease
  mutate(permease_centroid = round((((stop - start) / 2)  + start), 0)) %>%
  
  # remove the columns for gene location
  select(-start, -stop, -direction, -gene_num, -func, -isomer) %>%
  
  # rename the gene name and id to be permase specific, to allow merging with df with the other proteins (based on genome and contig)
  rename(permease_id = gene_id) %>%
  rename(permease = gene)


# find the best hits for each protein, merge with the proteases and calculate the distance to the protease
best_hit_distance_to_permease <- compiled_annotations %>%
  
  # remove permeases 
  filter(hmm_domain != "Lactate_perm") %>% 
  
  # select the characterized gene name with the highest bit score and only keep that single version
  # this should exlude hits to duplicated proteins and only look at the best hit (with all domains)
  group_by(genome, gene) %>%
  mutate(n_gene = length(unique(gene_id))) %>%
  mutate(max_bitscore_gene = max(bitscore)) %>%
  ungroup() %>%
  
  filter(bitscore == max_bitscore_gene) %>%
  
  # if a single protein hits two genes, only keep the best hit
  # since this is the same protein, it just select what gene gets assigned to it
  group_by(genome, gene_id) %>%
  mutate(max_bitscore_gene_id = max(bitscore)) %>%
  ungroup() %>%
  
  filter(bitscore == max_bitscore_gene_id) %>%
  
  # join with permease df
  inner_join(permease) %>%
  
  # calculate middle position of gene
  mutate(centroid = round((((stop - start) / 2)  + start), 0)) %>%
  
  # calculate distance to permease
  mutate(distance = centroid - permease_centroid) %>%
  mutate(distance_abs = abs(distance))


# create new labels combining genomes and a number for each permease
permease_num <- best_hit_distance_to_permease %>%
  select(genome, permease_id, permease_centroid, contig_id) %>%
  distinct() %>%
  
  # number each permease
  group_by(genome) %>%
  mutate(permease_num = seq_along(permease_id)) %>%
  ungroup() %>%
  
  # combine the permease number with the genome id
  unite(genome_permease_num, c("genome", "permease_num"), sep = "_", remove = FALSE) %>%
  
  select(-permease_num) 
  
  
  
  

# so far this code selects for only genomes with a lactate permease
# also only distance were the genes are on the same contig are shown
# this should be ok though if i only focus on genes surrounding the lactate permase
# i will start by looking with 10kB

plot_data <- best_hit_distance_to_permease %>%
  
  # join with the new label with numbered permaease
  inner_join(permease_num) %>%
  
  select(genome, genome_permease_num, contig_id, gene_id, gene, func, isomer, n_permease, permease_id, permease, distance_abs) %>%
  distinct() %>%
  
  # combine function and isomer into a annotation label for plotting
  unite(annotation, c("func", "isomer"), sep = " - ") %>%
  
  # select only genes within 10kB of a permease
  filter(distance_abs < distance_to_permease) %>%
  
  # count the number of genes that are within the 10kB of the permease
  group_by(genome, permease_id) %>%
  mutate(n_genes_near_permease = length(unique(gene))) %>%
  ungroup()  
  

# write plot data for the selected genes
write.csv(plot_data, "~/master/lactate/dataflow/04-analysis-tables/selected_genes.csv")

# extract the surrounding regions of the selected genes from a complete headers file
# this is to draw gene diagrams

# this allows me to simply subset the file based on the genomes I am working with to make 
# headers file smaller
genomes <- unique(plot_data$genome)
permeases <- unique(plot_data$permease_id)

# input headers file
prot_headers <- read_csv("~/master/lactate/dataflow/00-meta/all_prot_headers.csv")

# remove file extension to get genome name
prot_headers$genome <- gsub(file_extension, "", prot_headers$file)

# extract start, stop and direction, and seperate out contig id and gene number
prot_headers <- prot_headers %>%
  # remove useless index columns
  select(-X1, -index) %>%
  # sperate the prodial header to get start, stop and direction
  separate(`0`, into = c("rm", "start", "stop", "direction"), sep = " # ") %>%
  # remove the first part of the header 
  select(-rm) %>%
  # select only the genomes that were left over from the selected genes
  filter(genome %in% genomes) %>% 
  # seperate gene id into contig id and gene number on last underscore occurence
  extract(gene_id, c("contig_id","gene_num"), "(.*)_([^_]+)$", remove = FALSE)


# create data frame to join with headers to label the selected genes (included the permeases)
# df with labels of selected genes
gene_names <- plot_data %>%
  select(genome, contig_id, gene_id, gene, annotation) %>%
  distinct()

# df with labels of permease, rename columns to bind with gene_names
permease_names <- plot_data %>%
  select(genome, contig_id, permease_id, permease) %>%
  distinct() %>%
  rename(gene_id = permease_id) %>%
  rename(gene = permease)

# bind the dataframes above together
names <- bind_rows(gene_names, permease_names) %>%
  mutate(annotation = if_else(!(is.na(annotation)), annotation, "permease"))

prot_headers$start <- as.numeric(prot_headers$start)
prot_headers$stop <- as.numeric(prot_headers$stop)



permease_num_sub <- permease_num %>%
  filter(permease_id %in% permeases)

prot_headers_subset <- inner_join(prot_headers, permease_num_sub) %>%
  mutate(region_start = if_else(permease_centroid - distance_to_permease > 0, permease_centroid - 5000 , 0)) %>%
  mutate(region_stop = permease_centroid + distance_to_permease) %>%
  filter(start > region_start) %>%
  filter(stop < region_stop) %>%
  left_join(names) %>%
  mutate(annotation = if_else(!(is.na(annotation)), annotation, "other")) %>%
  mutate(gene = if_else(!(is.na(gene)), gene, "other")) #%>%
  #select(gene_id, start, stop, direction, gene) %>%
  #inner_join(colour_map) %>%
  #select(gene_id, start, stop, direction, colour, gene)

write.csv(prot_headers_subset, "~/master/lactate/dataflow/04-analysis-tables/gene_diagrams.csv")


#write.table(prot_headers_subset, "~/master/lactate/dataflow/04-analysis-tables/gene_diagrams.txt", sep = "\t", col.names = FALSE, row.names = FALSE)


