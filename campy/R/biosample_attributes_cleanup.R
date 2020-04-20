# sript to cleam up attribute list from biosample

# HARDCODED
file <- "dataflow/00-meta/campylobacter_sample_attributes.csv"
output <- "dataflow/00-meta/campylobacter_sample_attributes_clean.csv"

df_sample_attributes <- read.csv(file)
colnames(df_sample_attributes) <- c('biosample', 'attributes')

df_sample_attributes$attributes <- gsub('b\'', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub('b\"', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub('\\n\'', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub('\\n\"', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub('\\t', ';', df_sample_attributes$attributes, fixed = TRUE)

df_sample_attributes$attributes <- gsub(';missing', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';Missing', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';unknown', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';Unknown', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';none', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';None', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';not applicable', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';Not applicable', '', df_sample_attributes$attributes, fixed = TRUE)
df_sample_attributes$attributes <- gsub(';Not Applicable', '', df_sample_attributes$attributes, fixed = TRUE)


df_sample_attributes$attributes <- gsub(';', ' | ', df_sample_attributes$attributes, fixed = TRUE)

write.csv(df_sample_attributes, output, row.names = FALSE)