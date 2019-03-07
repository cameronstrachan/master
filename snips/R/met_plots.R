library(tidyverse)

df <- read.csv("~/master/rumen/dataflow/00-meta/Seshradi2015_pathways.csv")
df[is.na(df)] <- 0
df$Family.Order <- gsub(" ", "", df$Family.Order)

df <- df %>%
  group_by(Family.Order) %>%
  mutate(ngenomes = length(unique(Strain))) %>%
  ungroup() %>%
  gather(Type, Presence, -Culture.collection.., -Genus.Species, -Family.Order, -ngenomes, -Strain) %>%
  group_by(Family.Order, Type) %>%
  mutate(Type_per = (sum(Presence) / ngenomes)*100) %>%
  ungroup()

df_sub <- df %>%
  select(Family.Order, Type, Type_per) %>%
  distinct() %>%
  separate(Type, into = c("Category", "Compound"), sep = "_")

ggplot(df_sub, aes(x=reorder(Family.Order,Type_per), y=Type_per)) +
       geom_point(aes(colour = Category), size = 5) +
       theme() +
       theme(strip.text = element_text(size = 20),
             plot.title = element_text(size = 25),
             axis.text.x = element_text(angle = 90, hjust = 1, size = 20),
             axis.text.y = element_text(size = 20),
             axis.title.x = element_text(size = 20),
             axis.title.y = element_text(size = 20)) +
  facet_wrap(Compound ~ .)

df_prevo <- df %>%
  filter()
