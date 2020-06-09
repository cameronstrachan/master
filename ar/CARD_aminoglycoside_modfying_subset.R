library(tidyverse)

# card hits

df_card_hits <- read_csv("~/master/ar/dataflow/04-tables/CARD_hits_95_90.csv")

df_card_hits_aminoglycoside <- df_card_hits %>%
  filter(drug_class == "aminoglycoside antibiotic" & resistance_mechanism != "antibiotic efflux")

write.csv("~/master/ar/dataflow/04-tables/CARD_hits_30_60_aminoglycoside_moedifying.csv")