library(tidyverse)
library(reshape2)

### METADATA
### ONLY LOOK AT BACTERIA PRIMER

df_meta <- read.csv("~/master/rumen/dataflow/00-meta/henderson2015_fastq.csv")

df_meta <- df_meta %>%
  select(Experiment, LibraryName, GRCid, Simple.classification..animal., Age.classification..animal., Gender..animal., Forage.proportion..diet., Concentrate.proportion..diet., Forage.concentrate.category..diet., Starch.rich..diet., Pectin.rich...diet., Weeks.on.diet..diet.)

colnames(df_meta) <- c("sra_accession", "lib_name", "GRCid", "animal_class", "animal_age", "gender", "forage_proportion", "concentrate_proportion", "diet_category", "starch_rich", "pectin_rich", "week_on_diet")

df_meta <- df_meta %>%
  separate(lib_name, into = c("rm", "primer"), sep = "\\.") %>%
  rowwise() %>%
  mutate(bacteria_primer = substr(primer, 1, 1) == "B") %>%
  filter(bacteria_primer == TRUE) %>%
  select(-rm)

### CLASSIFICATION
### ONLY SEQUENCES CLASSIFIED AT PHYLUM LEVEL

df_classification  <- read.csv("~/master/rumen/dataflow/03-asv-taxonomy/henderson2015-20_320-98-rdp.csv")
df_classification[,1] <- NULL

df_classification <- df_classification %>%
  select(asv_id, phylum, family, genus) %>%
  filter(phylum != "NA")

### OTU TABLE

df <- read.delim("~/master/rumen/dataflow/03-asv-table/henderson2015-20_320-98.txt", skip = 1, header = TRUE)
df$clustering <- 97
colnames(df)[1] <- 'asv_id'

col_to_gather <- names(df)[!(startsWith(names(df), "SRX"))]
df <- melt(df, id = col_to_gather)
colnames(df)[3:4] <- c('sra_accession', 'count')

df$asv_id <- as.character(df$asv_id)

### SAMPLES ONLY WITH MORE THAN 1000 READS

df_normalization <- df %>%
  filter(clustering == 97) %>%
  group_by(sra_accession) %>%
  mutate(total_reads = sum(count)) %>%
  ungroup() %>%
  select(sra_accession, total_reads) %>%
  ungroup() %>%
  distinct() %>%
  filter(total_reads > 1000)


df_complete <- inner_join(df, df_meta) %>%
  inner_join(df_normalization) %>%
  inner_join(df_classification)

rm(list=setdiff(ls(), "df_complete"))

df_lacto_positive <- df_complete %>%
  filter(genus == "Lactobacillus") %>%
  mutate(count_norm = (count / total_reads)*100)  %>%
  filter(count_norm > 0.001)


lacto_positive_samples <- unique(df_lacto_positive$GRCid)

df_complete_starch <- df_complete %>%
  filter(starch_rich == "y") 


df_complete_starch <- df_complete_starch%>%
  rowwise() %>%
  mutate(lacto_signal = ifelse(GRCid %in% lacto_positive_samples, "pos", "neg")) %>%
  ungroup() 

df_metrics <- df_complete_starch %>% 
  
  mutate(count_norm = (count / total_reads)*100) %>%
  
  unite(classification, c("phylum", "family", "genus"), sep = ";", remove = FALSE) %>%
  
  distinct() 

write.csv(df_metrics, "~/master/rumen/dataflow/04-analysis-tables/henderson2015-20_320-98_df_metrics_lacto_1000.csv")