library(rRDP)
library(tidyverse)

seq <- readDNAStringSet("~/master/epithelial/dataflow/01-nucl/epithelial_cultured_strains_oneLine.fasta")
pred <- predict(rdp(), seq)
conf <- attr(pred, "confidence")

pred$fasta_header <- row.names(pred)
conf <- as.data.frame(conf)
colnames(conf) <- paste(colnames(conf), "conf", sep = "_")
conf$fasta_header <- row.names(conf)

df_taxa <- inner_join(pred, conf) %>%
  select(fasta_header, domain, domain_conf, phylum, phylum_conf, class, class_conf, order, order_conf, family, family_conf, genus, genus_conf)

write.csv(df_taxa, '~/master/epithelial/dataflow/04-classification/classification.csv')