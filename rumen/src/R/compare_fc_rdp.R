library(tidyverse)

df_gg <- read.delim("~/master/rumen/dataflow/03-asv-taxonomy/reddy2018-6_166-fc-gg-full.txt")
df_rdp <- read.csv("~/master/rumen/dataflow/03-asv-taxonomy/reddy2018-6_166-100-rdp.csv")


df_gg_clean <- df_gg %>% 
  rowwise() %>%
  separate(Taxon, into = c("domain", "phylum", "class", "order", "family", "genus"), sep = ";")


df_gg_clean$domain <- gsub("k__", "", df_gg_clean$domain)
df_gg_clean$phylum <- gsub("p__", "", df_gg_clean$phylum)
df_gg_clean$class <- gsub("c__", "", df_gg_clean$class)
df_gg_clean$order <- gsub("o__", "", df_gg_clean$order)
df_gg_clean$family <- gsub("f__", "", df_gg_clean$family)
df_gg_clean$genus <- gsub("g__", "", df_gg_clean$genus)

colnames(df_gg_clean)[1] <- "asv_id"


df_conf <- df_rdp[,9:14]

df_rdp_clean <- df_rdp %>%
  select(asv_id, 2:7)

df_rdp_clean$Confidence <- "NA"

for (i in 1:nrow(df_rdp_clean)){
  k <- 7
  if(is.na(df_rdp_clean[i,k])){
    k <- k - 1 
    if(is.na(df_rdp_clean[i,k])){
      k <- k - 1 
      if(is.na(df_rdp_clean[i,k])){
        k <- k - 1 
        if(is.na(df_rdp_clean[i,k])){
          k <- k - 1
          if(is.na(df_rdp_clean[i,k])){
            k <- k - 1 
            if(is.na(df_rdp_clean[i,k])){
              k <- k - 1 
            } else {
              conf <- k - 1
              df_rdp_clean[i,8] <- df_conf[i, conf] }
          } else {
            conf <- k - 1
            df_rdp_clean[i,8] <- df_conf[i, conf] }
          } else {
            conf <- k - 1
            df_rdp_clean[i,8] <- df_conf[i, conf] }
          } else {
            conf <- k - 1
            df_rdp_clean[i,8] <- df_conf[i, conf] }
          } else {
            conf <- k - 1
            df_rdp_clean[i,8] <- df_conf[i, conf] }
  } else {
    conf <- k - 1
    df_rdp_clean[i,8] <- df_conf[i, conf]
    
  }

}

### genus

df_rdp_clean_genus <-  df_rdp_clean %>%
  filter(genus != "NA") %>%
  select(asv_id, genus) %>%
  rename(genus_rdp = genus)

df_rdp_clean_genus$genus_rdp <- as.character(df_rdp_clean_genus$genus_rdp)
df_rdp_clean_genus$genus_rdp <- gsub(" ", "", df_rdp_clean_genus$genus_rdp)

df_gg_clean_genus <- df_gg_clean %>%
  filter(genus != "NA") %>%
  filter(genus != " ") %>%
  select(asv_id, genus) %>%
  rename(genus_gg = genus)

df_gg_clean_genus$genus_gg <- as.character(df_gg_clean_genus$genus_gg)
df_gg_clean_genus$genus_gg <- gsub(" ", "", df_gg_clean_genus$genus_gg)

df_genus <- inner_join(df_rdp_clean_genus, df_gg_clean_genus) %>%
  rowwise() %>%
  mutate(match = ifelse(genus_rdp == genus_gg, 1, 0))

(sum(df_genus$match) / nrow(df_genus)) * 100

### family

df_rdp_clean_family <-  df_rdp_clean %>%
  filter(family != "NA") %>%
  select(asv_id, family) %>%
  rename(family_rdp = family)

df_rdp_clean_family$family_rdp <- as.character(df_rdp_clean_family$family_rdp)
df_rdp_clean_family$family_rdp <- gsub(" ", "", df_rdp_clean_family$family_rdp)

df_gg_clean_family <- df_gg_clean %>%
  filter(family != "NA") %>%
  filter(family != " ") %>%
  select(asv_id, family) %>%
  rename(family_gg = family)

df_gg_clean_family$family_gg <- as.character(df_gg_clean_family$family_gg)
df_gg_clean_family$family_gg <- gsub(" ", "", df_gg_clean_family$family_gg)

df_family <- inner_join(df_rdp_clean_family, df_gg_clean_family) %>%
  rowwise() %>%
  mutate(match = ifelse(family_rdp == family_gg, 1, 0))

(sum(df_family$match) / nrow(df_family)) * 100

### phylum

df_rdp_clean_phylum <-  df_rdp_clean %>%
  filter(phylum != "NA") %>%
  select(asv_id, phylum) %>%
  rename(phylum_rdp = phylum)

df_rdp_clean_phylum$phylum_rdp <- as.character(df_rdp_clean_phylum$phylum_rdp)
df_rdp_clean_phylum$phylum_rdp <- gsub(" ", "", df_rdp_clean_phylum$phylum_rdp)

df_gg_clean_phylum <- df_gg_clean %>%
  filter(phylum != "NA") %>%
  filter(phylum != " ") %>%
  select(asv_id, phylum) %>%
  rename(phylum_gg = phylum)

df_gg_clean_phylum$phylum_gg <- as.character(df_gg_clean_phylum$phylum_gg)
df_gg_clean_phylum$phylum_gg <- gsub(" ", "", df_gg_clean_phylum$phylum_gg)

df_phylum <- inner_join(df_rdp_clean_phylum, df_gg_clean_phylum) %>%
  rowwise() %>%
  mutate(match = ifelse(phylum_rdp == phylum_gg, 1, 0))

(sum(df_phylum$match) / nrow(df_phylum)) * 100
