library(ggplot2)
library(tidyverse)

df <- read.csv("~/master/for_anna/Overview_kinetics_NOB.csv")
df <- df %>%
  filter(Strain != "Nitrobacter winogradskyi")

df$Strain <- factor(df$Strain, levels = as.character(df$Strain))


plot <- ggplot(df, aes(x=Strain)) +
  theme_gdocs() +
  geom_point(aes(y = Km),
             stat = "identity", fill = "lightgrey", size = 4) +
  theme(strip.text = element_text(size = 14),
        axis.text.y = element_text(size = 14), 
        axis.title.y = element_text(size = 16),
        axis.title.x = element_blank(),
        axis.text.x = element_text(angle = 90, hjust = 1, size = 14)) +
  ylab("Km") +
  geom_errorbar(aes(ymin=Km-SD, ymax=Km+SD), width=.2,
                position=position_dodge(.9)) 

plot
