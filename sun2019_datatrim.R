library(tidyverse)
library(party)
library(randomForest)
library(e1071)
library(stringr)
library(printr)
library(reshape2)
library(rpart)

df <- read.csv("~/Desktop/cow_test.csv")

df <- df %>%
  select(Rumen.pH, Acetate., Propionate., Isobutyrate., Butyrate., Isovalerate., NH3.N)

colnames(df) <- c("pH", "acetate", "propionate", "isobutyrate", "butyrate", "isovalerate", "NH3")

plot(df$pH ~ df$acetate) # 45 >
plot(df$pH ~ df$propionate) # > 9
plot(df$pH ~ df$butyrate) # > 5 < 20

