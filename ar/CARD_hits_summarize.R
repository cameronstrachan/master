library(data.table)
setDTthreads(10)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
 cutoff = 95
} else if (length(args)==1) {
  cutoff = as.numeric(args[1])
} else {
  stop("Only provide one argument!", call.=FALSE)
}



folder <- "~/master/ar/dataflow/03-blast/CARD/"
files <- list.files(folder, pattern = "\\.txt$")

df_list <- list()
i <- 1

for (file in files){

  input_file <- paste(folder, file, sep = "")
  df <- read.delim(input_file, header=FALSE)
  df <- data.table(df)
  
  if (nrow(df[V3 >= cutoff]) > 0){
    df_select = df[V3 >= cutoff]
    df_select = df_select[,.(V1,V2,V3,V11,V12)]
    df_list[[i]] <- df_select
    i <- i + 1
  }
  
}

df_complete <- rbindlist(df_list)

save_file <- paste("dataflow/04-tables/CARD_hits_", as.character(cutoff), ".csv", sep = "")

write.csv(df_complete, save_file)
