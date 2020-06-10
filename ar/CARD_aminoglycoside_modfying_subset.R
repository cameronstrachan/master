library(tidyverse)

# card hits
df_card_hits <- read_csv("~/master/ar/dataflow/04-tables/CARD_hits_30_60.csv")

df_card_hits_aminoglycoside <- df_card_hits %>%
  filter(drug_class == "aminoglycoside antibiotic" & resistance_mechanism != "antibiotic efflux")

# ANT
selected_rows <- grepl("ANT", df_card_hits_aminoglycoside$gene_family)
df_ants <- df_card_hits_aminoglycoside[selected_rows, ]

# APH
selected_rows <- grepl("APH", df_card_hits_aminoglycoside$gene_family)
df_aphs <- df_card_hits_aminoglycoside[selected_rows, ]

# save files
write.csv(df_card_hits_aminoglycoside, "~/master/ar/dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying.csv", row.names = FALSE)
write.csv(df_ants, "~/master/ar/dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying_ant.csv", row.names = FALSE)
write.csv(df_aphs, "~/master/ar/dataflow/04-tables/CARD_hits_30_60_aminoglycoside_modifying_aph.csv", row.names = FALSE)