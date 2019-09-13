library(tidyverse)

df_ph <- read.csv("~/master/rusitec/T48_pH.csv")
df_ph$Date <- NULL

df_ph_avg <- df_ph %>%
  gather(Reactor, pH, -Point, -Time, -Hour) %>%
  select(-Point, -Time) %>%
  group_by(Hour, Reactor) %>%
  mutate(ph_mean = mean(pH)) %>%
  ungroup() %>%
  select(-pH) %>%
  distinct()


df_vfa <- read.csv("~/master/rusitec/T48_VFAs.csv")
df_vfa <- df_vfa[-1,]
df_vfa$Point <- gsub("Rusitec-T48_", "", df_vfa$Point)

df_vfa <- df_vfa %>%
  separate(Point, into = c("Hour", "Reactor"), sep = "_")

df_vfa$Hour <- gsub("h", "", df_vfa$Hour)
df_vfa$Hour <- as.integer(df_vfa$Hour)

df_vfa$Reactor <- paste("R", df_vfa$Reactor, sep = "")

df_meta <- read.csv("~/master/rusitec/T48_meta.csv")

df_plot <- inner_join(df_ph_avg, df_vfa) %>%
  inner_join(df_meta) %>%
  gather(Measurement, Value, -Hour, -Group, -Reactor) %>%
  filter(Measurement == "Propionic.acid" | Measurement == "Valeric.acid" | Measurement == "ph_mean") %>%
  group_by(Hour, Group, Measurement) %>%
  mutate(Measurement_med = median(Value)) %>%
  ungroup()

library(ggplot2)

plot <- ggplot(df_plot, aes(x=Hour, y=Measurement_med, group=Group)) + 
  geom_point(aes(colour=Group)) + 
  facet_wrap(~Measurement, scales = "free_y") + 
  geom_smooth(aes(colour=Group))
plot
