library(data.table)

folder <- "~/master/ar/dataflow/03-blast/CARD/"
files <- list.files(folder, pattern = "\\.txt$")

df_list <- list()
i <- 1

for (file in files){

  input_file <- paste(folder, file, sep = "")
  df <- read.delim(input_file, header=FALSE)
  df <- data.table(df)
  
  if (nrow(df[V3 == 100]) > 0){
    df_select = df[V3 == 100]
    df_select = df_select[,.(V1,V2,V3,V11,V12)]
    df_list[[i]] <- df_select
    i <- i + 1
  }
  
}

df_complete <- rbindlist(df_list)
write.csv(df_complete, "~/master/ar/dataflow/04-tables/CARD_hits_100.csv")
